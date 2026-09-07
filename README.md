# TaxoSplitter — Vertical Router v1

**Map 2,000+ business categories to 11 master sales verticals using contrastive fine-tuning of sentence embeddings.**

TaxoSplitter takes a flat list of POI/business categories (e.g. from Google Maps, Yelp, or any CRM) and routes each one to the correct sales vertical — Healthcare, Automotive, Construction, Real Estate, Industrial, Facilities, Hospitality, Retail, Professional Services, Education, or Archive — using a fine-tuned [intfloat/e5-base-v2](https://huggingface.co/intfloat/e5-base-v2) model.

---

## The Problem

Off-the-shelf embedding models are **surprisingly bad** at mapping business categories to sales verticals. The root cause is **suffix poisoning** — generic English suffixes hijack the semantic signal and pull categories into the wrong domain.

**Real examples of suffix poisoning:**

| Category | Correct Vertical | Where It Lands (Zero-Shot) | Why |
|---|---|---|---|
| `power station` | V5_Industrial | V10_Education | "station" matches "fire station", "police station" → government/civic |
| `software company` | V9_Professional | V5_Industrial | "company" matches manufacturing/industrial language |
| `beauty product supplier` | V8_Retail | V5_Industrial | "supplier" overwhelms "beauty" and pulls toward supply chain |
| `smog inspection station` | V2_Automotive | V10_Education | "station" again — same trap, different category |
| `media company` | V9_Professional | V5_Industrial | "company" bias toward industrial sector |

The base model understands English perfectly well — it just doesn't understand **your taxonomy**. The word "station" means something specific in your sales context that it doesn't know yet.

---

## The Solution

Instead of writing 2,000 manual rules, we **teach the model your taxonomy** through contrastive fine-tuning:

1. **Start with a strong base** — `intfloat/e5-base-v2` is a 768-dimensional sentence embedding model designed for asymmetric retrieval (short query vs. long passage). It already understands language; it just doesn't understand your 11 verticals.

2. **Write rich domain descriptions** — Each of your 11 verticals gets a detailed multi-sentence description explaining what kinds of businesses belong there (`data/domains.py`).

3. **Run a zero-shot baseline** — Embed every category and every domain description, then assign each category to its nearest domain by cosine similarity. Most get it right. Some don't.

4. **Correct only the mistakes** — Review the low-confidence assignments. For each wrong one, record a `(category, correct_domain, wrong_domain)` tuple in `data/manual_corrections.py`. Typically 20–50 corrections is enough.

5. **Fine-tune with contrastive loss** — For each correction, create a positive pair (category ↔ correct domain, label=1.0) and a negative pair (category ↔ wrong domain, label=0.0). The model learns to reshape its embedding space so your verticals sit in the right places. High-confidence correct assignments are included as anchors to prevent catastrophic forgetting.

6. **Export a static lookup table** — After training, every category gets a permanent domain assignment saved as a JSON dictionary. At runtime, classification is a dictionary lookup (microseconds). New unseen categories can still use the trained model for inference (milliseconds).

**The result:** A complete `category → vertical` mapping with no suffix poisoning, no manual rules, and no LLM API costs at runtime.

---

## Project Structure

```
TaxoSplitter_VerticalRouter_v1/
│
├── train.ipynb                        # Main notebook — run this end-to-end
│
├── data/
│   ├── __init__.py                    # Package exports for clean imports
│   ├── categories.py                  # CATEGORIES — list of 2,024 business category strings
│   ├── domains.py                     # DOMAINS — dict of 11 verticals + ARCHIVE with rich descriptions
│   └── manual_corrections.py          # MANUAL_CORRECTIONS — list of (category, correct, wrong) tuples
│
├── model/                             # [Created at runtime] Fine-tuned e5-base-v2 model weights
│
├── outputs/
│   ├── baseline_results.json          # [Created at runtime] Zero-shot classification results
│   ├── final_mapping.json             # [Created at runtime] Final category → vertical lookup table
│   └── changes_report.json            # [Created at runtime] What changed after fine-tuning
│
├── figures/                           # [Created at runtime] Publication-ready plots at 300 DPI
│   ├── confidence_dist.png            # Baseline vs fine-tuned score distributions
│   ├── per_domain_accuracy.png        # Per-vertical accuracy comparison
│   ├── tsne_baseline.png              # t-SNE of baseline embedding space
│   ├── tsne_finetuned.png             # t-SNE of fine-tuned embedding space
│   └── suffix_analysis.png            # Suffix poisoning frequency and score analysis
│
├── eval_results/                      # [Created at runtime] Evaluation metrics
│
└── README.md                          # This file
```

---

## How It Works

### Phase 1 — Zero-Shot Baseline

The base `e5-base-v2` model embeds all 2,024 categories and all 11 domain descriptions into 768-dimensional vectors. Each category is assigned to the domain with the highest cosine similarity. Results are tagged as HIGH (>0.75), MEDIUM (0.60–0.75), or LOW (<0.60) confidence. This baseline tells you exactly where the model struggles before any training.

### Phase 2 — Build Training Examples

You review the baseline results (especially LOW and MEDIUM confidence ones) and record corrections in `data/manual_corrections.py`. The system then builds training pairs automatically: positive pairs pull a category toward its correct domain, negative pairs push it away from the wrong one, and high-confidence baseline results are added as anchors so the model doesn't forget what it already gets right.

### Phase 3 — Fine-Tune

The model is fine-tuned using `CosineSimilarityLoss` — a contrastive objective that adjusts embedding geometry so cosine similarity between a category and its correct domain approaches 1.0, while similarity to wrong domains approaches 0.0. Training runs for 4 epochs with a warmup schedule. The fine-tuned model is saved to `model/`.

### Phase 4 — Classify

The fine-tuned model re-classifies all 2,024 categories using the same cosine similarity approach as Phase 1. The improved results are saved as the final lookup table.

### Phase 5 — Compare

A side-by-side comparison of baseline vs. fine-tuned results shows exactly which categories changed domains and by how much. A confidence breakdown and full changes report are saved for analysis.

### Phase 6 — Production Usage

The final lookup table (`outputs/final_mapping.json`) is a static JSON dictionary. For known categories, classification is an instant dictionary lookup. For new unseen categories, the trained model performs live inference in milliseconds.

---

## How to Run on Google Colab

1. **Open Google Colab** — Go to [colab.research.google.com](https://colab.research.google.com)

2. **Switch to GPU runtime** — Click `Runtime` → `Change runtime type` → select **T4 GPU** → `Save`

3. **Clone the repository** — In the first cell, run:
   ```python
   !git clone https://github.com/YOUR_USERNAME/TaxoSplitter_VerticalRouter_v1.git
   %cd TaxoSplitter_VerticalRouter_v1
   ```

4. **Open the notebook** — Navigate to `train.ipynb` in the Colab file browser, or upload it directly

5. **Run all cells** — Click `Runtime` → `Run all`, or step through each cell:
   - Cell 0 installs dependencies and verifies GPU
   - Cells 1–7 run the full 6-phase pipeline
   - Cells 8–10 generate all research figures

6. **Download results** — After completion, download from:
   - `outputs/final_mapping.json` — your production lookup table
   - `outputs/changes_report.json` — what training changed
   - `figures/` — all publication-ready plots

---

## How to Add Your Own Categories

Open `data/categories.py` and replace the `CATEGORIES` list with your own:

```python
CATEGORIES = [
    "your category one",
    "your category two",
    "your category three",
    # ... add as many as you need
]
```

**Rules:**
- One category per line, lowercase, as a plain string
- No duplicates
- The list can be any length — 100 or 10,000 categories work the same way

---

## How to Add Manual Corrections

After running Phase 1 (zero-shot baseline), review `outputs/baseline_results.json`. Look for categories with `"confidence": "LOW"` or `"confidence": "MEDIUM"` that are assigned to the wrong domain.

Open `data/manual_corrections.py` and add your corrections:

```python
MANUAL_CORRECTIONS = [
    # (category_string,    correct_domain,     wrong_domain_it_got)
    ("power station",       "V5_Industrial",    "V10_Education"),
    ("software company",    "V9_Professional",  "V5_Industrial"),
    ("beauty product supplier", "V8_Retail",    "V5_Industrial"),
    # Add more as you find them...
]
```

**Tips:**
- You typically need 20–50 corrections for good results
- Focus on categories where the suffix is misleading (station, company, supplier, service)
- After adding corrections, re-run the notebook from Phase 2 onward

---

## Output Files

| File | Contains | How to Use |
|---|---|---|
| `outputs/baseline_results.json` | Every category's zero-shot assignment, score, confidence, and per-domain score breakdown | Review to find misclassifications and build manual corrections |
| `outputs/final_mapping.json` | Every category's final assignment after fine-tuning (domain, score, confidence) | **This is your production lookup table.** Load it as a Python dict for instant classification |
| `outputs/changes_report.json` | Summary of what changed: total changed count, confidence breakdown, and per-category before/after | Audit training impact and verify corrections took effect |
| `model/` | Fine-tuned e5-base-v2 model weights | Load with `SentenceTransformer("./model")` to classify new unseen categories |
| `figures/*.png` | Publication-ready plots at 300 DPI | Include directly in research papers or presentations |

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `sentence-transformers` | ≥2.2.0 | Model loading, training, and inference |
| `torch` | ≥2.0.0 | Neural network backend |
| `datasets` | ≥2.0.0 | HuggingFace dataset utilities |
| `numpy` | ≥1.21.0 | Numerical operations |
| `matplotlib` | ≥3.5.0 | All figure generation |
| `scikit-learn` | ≥1.0.0 | t-SNE dimensionality reduction |

Install all at once:

```bash
pip install sentence-transformers torch datasets numpy matplotlib scikit-learn
```

---

## License

MIT
