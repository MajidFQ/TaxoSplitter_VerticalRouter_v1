#!/usr/bin/env python3
"""
groq_labeler.py
───────────────
Sends all CATEGORIES to Groq in batches and gets the LLM to map each one
to the correct domain key from DOMAINS. Saves the result as ground_truth.json.

Setup:
    pip install groq python-dotenv

    Then create a .env file in this folder with:
        GROQ_API_KEY=gsk_your_key_here

    Get your key at: https://console.groq.com/keys

Usage:
    python groq_labeler.py              # full run
    python groq_labeler.py --resume     # resume a partial run
    python groq_labeler.py --batch-size 15 --model openai/gpt-oss-120b
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path

# ── Groq SDK ─────────────────────────────────────────────────────────────────
try:
    from groq import Groq
except ImportError:
    print("ERROR: groq package not installed. Run: pip install groq")
    sys.exit(1)

# ── Load project data ─────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from data.categories import CATEGORIES
from data.domains import DOMAINS

# ── Config ───────────────────────────────────────────────────────────────────
MODEL          = "openai/gpt-oss-120b"  # 120B model (JSON mode fixed, batch size keeps TPM < 8k)
BATCH_SIZE     = 15                          # Safe size: ~1,200 tokens/call total
DELAY_SECONDS  = 5.0                         # 5s between batches
MAX_RETRIES    = 5
OUTPUT_FILE    = "data/ground_truth.json"
DOMAIN_KEYS    = list(DOMAINS.keys())


# ── System prompt (built ONCE, not per batch) ────────────────────────────────
def _extract_rule(desc: str) -> str:
    """
    Pull the full RULE sentence from a domain description.
    The RULE: line may wrap across multiple lines until a blank line.
    """
    lines = desc.strip().splitlines()
    collecting = False
    rule_parts = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("RULE:"):
            collecting = True
            rule_parts.append(stripped[5:].strip())
        elif collecting:
            # Stop at blank line or next section keyword
            if not stripped or stripped.startswith("INCLUDES:") or stripped.startswith("DOES NOT"):
                break
            rule_parts.append(stripped)
    if rule_parts:
        return " ".join(rule_parts)
    # fallback
    for line in lines:
        if line.strip():
            return line.strip()
    return desc.strip()[:150]


def _build_system_prompt() -> str:
    """
    Compact system prompt: one RULE line per domain only.
    Full domain descriptions are ~2,500 tokens each call — way too expensive.
    The RULE line is enough for the 120B model to classify correctly.
    """
    rules_block = "\n".join(
        f"{key}: {_extract_rule(desc)}"
        for key, desc in DOMAINS.items()
    )
    return f"""You are a business taxonomy classifier. Assign each business category string to exactly one domain key.

Domain keys and their one-line rules:
{rules_block}

OUTPUT RULES:
- Return ONLY a valid JSON object. No markdown, no explanation, no code block.
- Every key must be the exact category string from the input (copy it verbatim).
- Every value must be exactly one domain key from the list above.
- Every category in the input must appear in the output.

Example output:
{{"pizza restaurant": "D07_FoodDining", "auto repair shop": "D03_Automotive", "software company": "D12_B2BCorporate"}}"""


# Build once at import time
_SYSTEM_PROMPT = _build_system_prompt()


def build_user_prompt(batch: list) -> str:
    items = "\n".join(f'- "{cat}"' for cat in batch)
    return f"Classify each of these business categories:\n\n{items}"


def _extract_json(text: str) -> dict:
    """
    Parse JSON from model output.
    Handles plain JSON and ```json ... ``` fenced blocks.
    """
    text = text.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"```$", "", text.strip())
    # Find the first { ... } block
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end+1]
    return json.loads(text)


# ── Core labeling function ────────────────────────────────────────────────────
def label_batch(client, batch: list, batch_num: int) -> dict:
    """Call Groq API for one batch. Returns {category: domain_key} dict."""
    attempt = 0
    while attempt < MAX_RETRIES:
        attempt += 1
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user",   "content": build_user_prompt(batch)},
                ],
                temperature=0.0,   # fully deterministic
                max_tokens=2048,   # enough room for 15 items + any padding
                # NOTE: response_format json_object removed — not supported by all Groq models
            )
            raw = response.choices[0].message.content.strip()
            result = _extract_json(raw)

            # Validate
            missing = [c for c in batch if c not in result]
            invalid = [v for v in result.values() if v not in DOMAIN_KEYS]

            if missing:
                print(f"    ⚠ attempt {attempt}: {len(missing)} missing — retrying")
                if attempt < MAX_RETRIES:
                    time.sleep(2 * attempt)
                    continue

            if invalid:
                print(f"    ⚠ attempt {attempt}: invalid keys {invalid} — retrying")
                if attempt < MAX_RETRIES:
                    time.sleep(2 * attempt)
                    continue

            # Drop any hallucinated keys, fill missing with None
            cleaned = {k: v for k, v in result.items() if k in batch and v in DOMAIN_KEYS}
            for cat in batch:
                if cat not in cleaned:
                    cleaned[cat] = None

            return cleaned

        except json.JSONDecodeError as e:
            print(f"    ✗ attempt {attempt}: JSON error — {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)

        except Exception as e:
            err_str = str(e)
            if "rate_limit" in err_str.lower() or "429" in err_str:
                # Read the actual retry-after from Groq's error message
                m = re.search(r"try again in ([\d.]+)s", err_str, re.IGNORECASE)
                wait = float(m.group(1)) + 3 if m else 65
                print(f"    ✗ Rate limit hit. Waiting {wait:.0f}s (Groq says so)...")
                time.sleep(wait)
                attempt -= 1  # don't count rate-limit waits as a real attempt
            else:
                print(f"    ✗ attempt {attempt}: {type(e).__name__}: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(3 ** attempt)  # 3, 9, 27, 81s

    print(f"    ✗ Batch {batch_num}: all retries exhausted. Marking as None.")
    return {cat: None for cat in batch}


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Label CATEGORIES via Groq LLM")
    parser.add_argument("--resume", action="store_true",
                        help="Skip already-labeled categories from a previous run")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                        help=f"Categories per API call (default {BATCH_SIZE})")
    parser.add_argument("--model", type=str, default=MODEL,
                        help=f"Groq model to use (default {MODEL})")
    parser.add_argument("--delay", type=float, default=DELAY_SECONDS,
                        help=f"Seconds between batches (default {DELAY_SECONDS})")
    args = parser.parse_args()

    # ── API key: .env file first, then env var ────────────────────────────────
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found.\n")
        print("  Option 1 — .env file (recommended):")
        print("    Create a file called .env in this folder:")
        print("      GROQ_API_KEY=gsk_your_key_here\n")
        print("  Option 2 — environment variable:")
        print("    export GROQ_API_KEY='gsk_your_key_here'\n")
        print("  Get your key at: https://console.groq.com/keys")
        sys.exit(1)

    client = Groq(api_key=api_key)
    os.makedirs("outputs", exist_ok=True)

    # ── Resume: load existing results ─────────────────────────────────────────
    existing = {}
    if args.resume and Path(OUTPUT_FILE).exists():
        with open(OUTPUT_FILE) as f:
            existing = json.load(f)
        done  = sum(1 for v in existing.values() if v is not None)
        fails = sum(1 for v in existing.values() if v is None)
        print(f"Resuming: {done} done, {fails} failed, "
              f"{len(CATEGORIES) - len(existing)} not yet seen.")

    # ── Which categories still need labeling ──────────────────────────────────
    if args.resume:
        to_label = [c for c in CATEGORIES if existing.get(c) is None]
    else:
        to_label = list(CATEGORIES)
        existing = {}

    if not to_label:
        print("All categories already labeled.")
        print(f"Output: {OUTPUT_FILE}")
        return

    batch_size = args.batch_size
    batches    = [to_label[i:i+batch_size] for i in range(0, len(to_label), batch_size)]
    total      = len(batches)
    results    = dict(existing)

    # Estimate tokens: ~15 tokens/category in user prompt + ~500 token system prompt
    est_tpm = (batch_size * 15 + 500) * (60 / (args.delay + 2))
    print(f"\n{'='*60}")
    print(f"Groq Batch Labeler")
    print(f"{'='*60}")
    print(f"  Model        : {args.model}")
    print(f"  Categories   : {len(to_label)}")
    print(f"  Batch size   : {batch_size}")
    print(f"  Batches      : {total}")
    print(f"  Delay        : {args.delay}s")
    print(f"  Est. TPM     : ~{est_tpm:,.0f}")
    print(f"  Output       : {OUTPUT_FILE}")
    print(f"{'='*60}\n")

    for i, batch in enumerate(batches, 1):
        print(f"Batch {i}/{total}  ({len(batch)} items)...", end=" ", flush=True)
        t0 = time.time()

        batch_result = label_batch(client, batch, i)
        results.update(batch_result)

        ok  = sum(1 for c in batch if results.get(c) is not None)
        bad = len(batch) - ok
        print(f"✓ {ok} ok  {bad} failed  [{time.time()-t0:.1f}s]")

        # Crash-safe save after every batch
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2)

        if i < total:
            time.sleep(args.delay)

    # ── Final report ──────────────────────────────────────────────────────────
    total_ok   = sum(1 for v in results.values() if v is not None)
    total_fail = sum(1 for v in results.values() if v is None)

    print(f"\n{'='*60}")
    print(f"DONE  —  {total_ok} labeled  /  {total_fail} failed")
    print(f"Output: {OUTPUT_FILE}")
    print(f"{'='*60}")

    from collections import Counter
    dist = Counter(v for v in results.values() if v is not None)
    print("\nDomain distribution:")
    for domain in DOMAIN_KEYS:
        count = dist.get(domain, 0)
        bar   = "█" * (count // 10)
        print(f"  {domain:<28} {count:>4}  {bar}")

    if total_fail > 0:
        print(f"\n⚠  {total_fail} failed — run with --resume to retry.")


if __name__ == "__main__":
    main()
