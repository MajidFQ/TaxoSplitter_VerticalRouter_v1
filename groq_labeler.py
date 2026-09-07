#!/usr/bin/env python3
"""
groq_labeler.py
───────────────
Sends all CATEGORIES to Groq in batches and gets the LLM to map each one
to the correct domain key from DOMAINS. Saves the result as ground_truth.json.

Usage:
    pip install groq
    export GROQ_API_KEY="gsk_..."
    python groq_labeler.py

    # Or pass key inline:
    GROQ_API_KEY="gsk_..." python groq_labeler.py

    # Resume a partial run (skips already-labeled categories):
    python groq_labeler.py --resume
"""

import os
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
MODEL          = "llama-3.3-70b-versatile"   # best available on Groq
BATCH_SIZE     = 50                           # categories per API call
DELAY_SECONDS  = 1.5                          # pause between batches (rate limit)
MAX_RETRIES    = 4                            # retries per batch on failure
OUTPUT_FILE    = "outputs/ground_truth.json"
DOMAIN_KEYS    = list(DOMAINS.keys())

# ── System prompt ─────────────────────────────────────────────────────────────
def build_system_prompt() -> str:
    domain_block = "\n\n".join(
        f"[{key}]\n{desc.strip()}"
        for key, desc in DOMAINS.items()
    )
    keys_str = ", ".join(DOMAIN_KEYS)
    return f"""You are a business taxonomy classifier. Your job is to assign each business category to exactly one of the following domain keys:

{keys_str}

Here are the definitions for each domain:

{domain_block}

RULES:
- You must return ONLY a valid JSON object.
- Keys are the exact category strings I give you.
- Values are exactly one of the domain keys listed above.
- Do not add explanations, markdown, or any text outside the JSON object.
- Do not make up new domain keys.
- Every category in the input must appear in the output.

Example output format:
{{
  "pizza restaurant": "V7_Hospitality",
  "auto repair shop": "V2_Automotive",
  "software company": "V9_Professional"
}}"""


def build_user_prompt(batch: list[str]) -> str:
    items = "\n".join(f'- "{cat}"' for cat in batch)
    return f"Classify each of these business categories:\n\n{items}"


# ── Core labeling function ────────────────────────────────────────────────────
def label_batch(client: Groq, batch: list[str], batch_num: int) -> dict[str, str]:
    """Call Groq API for one batch. Returns {category: domain_key} dict."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": build_system_prompt()},
                    {"role": "user",   "content": build_user_prompt(batch)},
                ],
                temperature=0.0,        # deterministic — we want no creativity here
                max_tokens=4096,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content.strip()
            result = json.loads(raw)

            # Validate: all keys present, all values are valid domain keys
            missing  = [c for c in batch if c not in result]
            invalid  = [v for v in result.values() if v not in DOMAIN_KEYS]

            if missing:
                print(f"    ⚠ Batch {batch_num} attempt {attempt}: {len(missing)} categories missing from response")
                # fill missing with None so we can retry
                if attempt < MAX_RETRIES:
                    time.sleep(2 ** attempt)
                    continue

            if invalid:
                print(f"    ⚠ Batch {batch_num} attempt {attempt}: invalid domain keys: {invalid}")
                if attempt < MAX_RETRIES:
                    time.sleep(2 ** attempt)
                    continue

            # Clean: drop any keys the LLM invented that aren't in our batch
            cleaned = {k: v for k, v in result.items() if k in batch and v in DOMAIN_KEYS}

            # Fill any remaining missing with None (will be retried in --resume mode)
            for cat in batch:
                if cat not in cleaned:
                    cleaned[cat] = None

            return cleaned

        except json.JSONDecodeError as e:
            print(f"    ✗ Batch {batch_num} attempt {attempt}: JSON parse error — {e}")
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)

        except Exception as e:
            err_str = str(e)
            if "rate_limit" in err_str.lower() or "429" in err_str:
                wait = 60
                print(f"    ✗ Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    ✗ Batch {batch_num} attempt {attempt}: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(2 ** attempt)

    # All retries exhausted — return Nones for this batch
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
    args = parser.parse_args()

    # ── API key ───────────────────────────────────────────────────────────────
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not set.")
        print("  Set it with:  export GROQ_API_KEY='gsk_...'")
        sys.exit(1)

    client = Groq(api_key=api_key)

    # ── Directory setup ───────────────────────────────────────────────────────
    os.makedirs("outputs", exist_ok=True)

    # ── Resume: load existing results ─────────────────────────────────────────
    existing: dict[str, str] = {}
    if args.resume and Path(OUTPUT_FILE).exists():
        with open(OUTPUT_FILE) as f:
            existing = json.load(f)
        already_done = sum(1 for v in existing.values() if v is not None)
        print(f"Resuming: {already_done} already labeled, "
              f"{len(existing) - already_done} failed (None), "
              f"{len(CATEGORIES) - len(existing)} not yet seen.")

    # ── Decide which categories need labeling ─────────────────────────────────
    if args.resume:
        to_label = [c for c in CATEGORIES if existing.get(c) is None]
    else:
        to_label = list(CATEGORIES)
        existing = {}

    if not to_label:
        print("All categories already labeled. Nothing to do.")
        print(f"Output: {OUTPUT_FILE}")
        return

    # ── Batch loop ────────────────────────────────────────────────────────────
    batch_size = args.batch_size
    batches = [to_label[i:i+batch_size] for i in range(0, len(to_label), batch_size)]
    total   = len(batches)
    results = dict(existing)

    print(f"\n{'='*60}")
    print(f"Groq Batch Labeler")
    print(f"{'='*60}")
    print(f"  Model      : {args.model}")
    print(f"  Categories : {len(to_label)}")
    print(f"  Batch size : {batch_size}")
    print(f"  Batches    : {total}")
    print(f"  Output     : {OUTPUT_FILE}")
    print(f"{'='*60}\n")

    for i, batch in enumerate(batches, 1):
        print(f"Batch {i}/{total}  ({len(batch)} categories) ...", end=" ", flush=True)
        t0 = time.time()

        batch_result = label_batch(client, batch, i)
        results.update(batch_result)

        # Count successes in this batch
        ok  = sum(1 for c in batch if results.get(c) is not None)
        bad = len(batch) - ok
        elapsed = time.time() - t0
        print(f"✓ {ok} labeled, {bad} failed  [{elapsed:.1f}s]")

        # Save after every batch (crash-safe)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, indent=2)

        # Rate limit pause (skip after last batch)
        if i < total:
            time.sleep(DELAY_SECONDS)

    # ── Final report ─────────────────────────────────────────────────────────
    total_labeled = sum(1 for v in results.values() if v is not None)
    total_failed  = sum(1 for v in results.values() if v is None)

    print(f"\n{'='*60}")
    print(f"DONE")
    print(f"  Total labeled : {total_labeled} / {len(CATEGORIES)}")
    print(f"  Failed (None) : {total_failed}")
    print(f"  Output file   : {OUTPUT_FILE}")
    print(f"{'='*60}")

    # Domain distribution
    from collections import Counter
    dist = Counter(v for v in results.values() if v is not None)
    print("\nDomain distribution:")
    for domain in DOMAIN_KEYS:
        count = dist.get(domain, 0)
        bar   = "█" * (count // 10)
        print(f"  {domain:<22} {count:>4}  {bar}")

    if total_failed > 0:
        failed_cats = [c for c, v in results.items() if v is None]
        print(f"\n⚠  {total_failed} categories could not be labeled:")
        for cat in failed_cats:
            print(f"   - {cat}")
        print(f"\nRun with --resume to retry failed ones.")


if __name__ == "__main__":
    main()
