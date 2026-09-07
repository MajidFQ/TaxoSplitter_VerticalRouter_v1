# Training Guide

A beginner-friendly guide for someone who has never trained a machine learning model before.

---

## What is an Embedding?

An embedding is a way to turn text into a list of numbers.

Imagine you have a dictionary where every word or phrase gets a "coordinate" in a huge map. Similar things end up close together on the map, and different things end up far apart. The phrase "Italian restaurant" would be close to "pizza restaurant" but far from "auto repair shop."

In this project, we use a model called **e5-base-v2** that turns any text into a list of **768 numbers**. These 768 numbers are the embedding — they're the text's coordinates in a 768-dimensional space. You can't visualize 768 dimensions, but the math works the same as a regular map: things that mean similar things have similar coordinates.

**Why this matters:** We turn each business category ("pizza restaurant") and each sales vertical description ("Businesses providing in-person dining…") into embeddings, then check which vertical each category is closest to.

---

## What is Cosine Similarity?

Cosine similarity measures how much two embeddings "point in the same direction."

**Simple analogy:** Imagine two arrows on a piece of paper. If both arrows point in the exact same direction, their cosine similarity is **1.0** (perfect match). If they point in opposite directions, it's **-1.0** (complete mismatch). If they're perpendicular (90°), it's **0.0** (unrelated).

In practice:
- **0.85** = very similar (e.g., "dentist" ↔ Healthcare vertical)
- **0.70** = somewhat similar (the model is uncertain)
- **0.55** = weakly similar (the model is probably wrong)

We use cosine similarity to assign each business category to whichever sales vertical it "points toward" most strongly.

---

## Why General Embeddings Fail Here

The e5-base-v2 model is trained on billions of sentences from the internet. It understands English very well. But it doesn't understand **your specific sales taxonomy.**

The problem is **suffix poisoning.** Many business categories end with generic English words that carry strong semantic signals in the wrong direction:

| Category | The suffix | What happens |
|---|---|---|
| `power station` | "station" | The model sees "station" and thinks police station, fire station → government/education |
| `software company` | "company" | The model sees "company" and thinks manufacturing company → industrial |
| `beauty product supplier` | "supplier" | The model sees "supplier" and thinks industrial supply chain → industrial |

The model isn't stupid — it correctly understands what "station" means in general English. The problem is that in **your taxonomy**, "power station" belongs in Industrial, not Education. The model doesn't know your rules because it was never taught them.

This is why we need fine-tuning.

---

## What Fine-tuning Does

Fine-tuning is like giving the model a short tutoring session on your specific taxonomy.

The model already knows English — it has read billions of sentences. We don't need to teach it language from scratch. We just need to **nudge** its understanding so that:

- "power station" gets pulled **toward** the Industrial vertical description
- "power station" gets pushed **away from** the Education vertical description

Think of it like adjusting the settings on a camera. The lens is already good — we're just fine-tuning the focus for our specific subject.

After fine-tuning:
- The model's 768-dimensional "map" shifts slightly
- Categories that were in the wrong neighborhood move to the right one
- Categories that were already correct stay where they are

The nudging is small and targeted. We're not rewriting the model — we're just adjusting where your 11 verticals sit in the model's internal map.

---

## What Contrastive Learning Is

Contrastive learning teaches the model by showing it **pairs of examples** and telling it whether each pair should be similar or different.

**Positive pair (should be similar):**
> "power station" + Industrial vertical description → label: **1.0**
>
> "These should be close together on the map."

**Negative pair (should be different):**
> "power station" + Education vertical description → label: **0.0**
>
> "These should be far apart on the map."

The model adjusts its internal weights so that the positive pairs end up closer together and the negative pairs end up further apart. After seeing enough pairs, the model's map reorganizes so that your taxonomy makes sense.

We also include **anchor pairs** — categories the model already gets right with high confidence. These tell the model "don't move these, you already got them right." This prevents the model from accidentally breaking things that already work while fixing the things that don't.

---

## Step by Step: Your First Training Run

### Step 1: Open Google Colab

Go to [colab.research.google.com](https://colab.research.google.com) in your browser. Sign in with your Google account.

### Step 2: Switch to GPU

Click **Runtime** → **Change runtime type** → Select **T4 GPU** → Click **Save**.

This gives you a free GPU that makes training much faster (~2 minutes instead of ~15 minutes).

### Step 3: Upload or Clone the Project

**Option A — Upload:** Click the folder icon on the left sidebar, then drag and drop the entire `TaxoSplitter_VerticalRouter_v1` folder.

**Option B — Clone from GitHub:**
```python
!git clone https://github.com/YOUR_USERNAME/TaxoSplitter_VerticalRouter_v1.git
%cd TaxoSplitter_VerticalRouter_v1
```

### Step 4: Open the Notebook

Double-click `train.ipynb` in the file browser to open it.

### Step 5: Run Cell 0 — Colab Setup

Click the ▶️ play button on the first cell. This installs all dependencies and checks for GPU. Wait for it to finish. You should see:

```
CUDA available: True
GPU: Tesla T4
Directory structure ready.
```

### Step 6: Run Cell 1 — Imports

Click ▶️. This loads all libraries and your data. You should see:

```
Loaded 2024 categories
Loaded 12 domains
Loaded 0 manual corrections
```

### Step 7: Run Cell 2 — Phase 1 (Zero-Shot Baseline)

Click ▶️. This runs the baseline classification. It takes ~1–2 minutes. When it finishes, you'll see every category grouped by domain with its score.

### Step 8: Review the Baseline

Open `outputs/baseline_results.json` in the Colab file browser. Look for categories with `"confidence": "LOW"` or `"confidence": "MEDIUM"`. Write down any that are assigned to the wrong domain.

### Step 9: Add Corrections (Optional for First Run)

If you found misclassifications, edit `data/manual_corrections.py` and add them. See the "How to Write Manual Corrections" section below. For your very first run, you can skip this step and come back later.

### Step 10: Run Cells 3–7 (Phases 2–6)

Click ▶️ on each cell in order. Phase 3 (fine-tuning) takes ~2 minutes on GPU.

### Step 11: Get Your Results

When Cell 7 finishes, your production lookup table is at `outputs/final_mapping.json`. Download it by right-clicking the file in the Colab file browser → **Download**.

### Step 12: Generate Figures (Optional)

Run Cells 9–10 to generate all research figures in the `figures/` folder.

---

## How to Read baseline_results.json

Open the file and you'll see entries like this:

```json
{
  "pizza restaurant": {
    "domain": "V7_Hospitality",
    "score": 0.8234,
    "confidence": "HIGH",
    "all_scores": {
      "V1_Healthcare": 0.4123,
      "V2_Automotive": 0.3891,
      "V7_Hospitality": 0.8234,
      ...
    }
  }
}
```

### What the confidence levels mean:

**HIGH (score > 0.75)** — The model is confident and almost certainly correct. No action needed. Example: "pizza restaurant" → V7_Hospitality at 0.82.

**MEDIUM (score 0.60–0.75)** — The model is uncertain. Check if the assignment is correct. If it is, leave it alone. If it's wrong, add a correction. Example: "software company" → V5_Industrial at 0.67 (wrong — should be V9_Professional).

**LOW (score < 0.60)** — The model is guessing. Almost always needs review. The `all_scores` field shows you which other domains were close. Example: "power station" → V10_Education at 0.54 (wrong — should be V5_Industrial).

### What to do:

1. **Filter for LOW and MEDIUM:** Search the JSON for `"confidence": "LOW"` and `"confidence": "MEDIUM"`
2. **Check each one:** Is the assigned domain correct?
3. **If wrong:** Note the category, the correct domain, and the wrong domain it got
4. **Add to corrections:** Put each wrong one in `data/manual_corrections.py`

---

## How to Write Manual Corrections

Open `data/manual_corrections.py` and add entries in this format:

```python
MANUAL_CORRECTIONS = [
    # (category_string,           correct_domain,      wrong_domain_it_got)
    ("power station",             "V5_Industrial",     "V10_Education"),
    ("software company",          "V9_Professional",   "V5_Industrial"),
    ("beauty product supplier",   "V8_Retail",         "V5_Industrial"),
    ("police station",            "V10_Education",     "V3_Construction"),
    ("media company",             "V9_Professional",   "V5_Industrial"),
]
```

### Rules:

- **Category string** must match exactly what's in `data/categories.py` (lowercase, same spelling)
- **Correct domain** is where the category **should** go (must be a key in `data/domains.py`)
- **Wrong domain** is where the baseline model **actually put it** (check `baseline_results.json`)
- Each entry is a tuple of 3 strings inside the list
- You typically need **20–50 corrections** for good results
- Focus on the **systematic errors** — suffixes that affect many categories

### Valid domain names:

```
V1_Healthcare, V2_Automotive, V3_Construction, V4_RealEstate,
V5_Industrial, V6_Facilities, V7_Hospitality, V8_Retail,
V9_Professional, V10_Education, ARCHIVE
```

---

## How to Know When Training Worked

After running all phases, look at the Phase 5 (Compare) output. Here's what to check:

### ✅ Training worked if:

- **Categories you corrected moved to the right domain.** If you said "power station" should be Industrial, it should now show Industrial in the final results.
- **The HIGH confidence count went up.** More categories should be HIGH confidence after training.
- **The LOW confidence count went down.** Fewer categories should be uncertain.
- **The total number of changed categories is reasonable.** Typically 30–150 categories will change. If 0 changed, your corrections might not have been loaded. If 1,000+ changed, something went wrong.

### ⚠️ Training might need adjustment if:

- **Some corrected categories didn't move.** The model may need more training examples for that particular pattern. Try adding more corrections for similar categories.
- **Categories you didn't correct also moved to wrong domains.** The model may have overcorrected. Try reducing epochs from 4 to 2.
- **The mean score dropped overall.** The contrastive loss may be too aggressive. Try adding more high-confidence anchor pairs.

### ❌ Something went wrong if:

- **0 categories changed.** Check that `data/manual_corrections.py` has entries and is being imported correctly.
- **All categories map to the same domain.** The model collapsed. Reduce epochs or increase batch size.
- **Scores are all very low (< 0.5).** The model's embedding space was damaged. Start fresh from the base model.

---

## Common Errors and Fixes

### "CUDA not available" / No GPU detected

**What it means:** Colab didn't assign you a GPU.

**Fix:**
1. Click **Runtime** → **Change runtime type**
2. Select **T4 GPU** from the dropdown
3. Click **Save**
4. The notebook will restart — run cells from the beginning

If T4 is unavailable, try again later (free GPU availability varies).

### "CUDA out of memory" / OOM Error

**What it means:** The GPU doesn't have enough memory for the current batch size.

**Fix:** In the fine-tuning cell (Phase 3), change `batch_size=16` to `batch_size=8`:

```python
train_dataloader = DataLoader(
    training_examples,
    shuffle=True,
    batch_size=8   # Reduced from 16
)
```

### "ModuleNotFoundError: No module named 'sentence_transformers'"

**What it means:** Dependencies weren't installed.

**Fix:** Run the Colab Setup cell (Cell 0) first. Make sure it finishes without errors.

### "ModuleNotFoundError: No module named 'data'"

**What it means:** The notebook can't find the `data/` folder.

**Fix:** Make sure you're running from the project root directory. In Colab:
```python
%cd /content/TaxoSplitter_VerticalRouter_v1
```

### "KeyError: 'V5_Industrial'" (or any domain name)

**What it means:** A domain name in your corrections doesn't match the domain names in `data/domains.py`.

**Fix:** Check spelling. Domain names are case-sensitive and must include the prefix: `V5_Industrial`, not `Industrial` or `v5_industrial`.

### "KeyError: 'power station'" (or any category)

**What it means:** A category in your corrections doesn't exist in `data/categories.py`.

**Fix:** Check spelling. Categories must be lowercase and match exactly.

### Training finishes but 0 categories changed

**What it means:** Either `MANUAL_CORRECTIONS` is empty or wasn't imported correctly.

**Fix:**
1. Check that `data/manual_corrections.py` has entries (not an empty list)
2. Check the import cell output — it should say `Loaded N manual corrections` where N > 0
3. Make sure you saved the file after editing

### Figures cell crashes with "No display"

**What it means:** Matplotlib is trying to open a GUI window in a headless environment.

**Fix:** This should be handled by `matplotlib.use('Agg')` in the imports cell. If you still get the error, add this before any plotting:
```python
import matplotlib
matplotlib.use('Agg')
```
