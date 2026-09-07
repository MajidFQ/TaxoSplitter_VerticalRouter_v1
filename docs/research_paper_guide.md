# Research Paper Guide

A practical guide for writing an academic paper using TaxoSplitter results.

---

## What to Document

Before writing, make sure you have collected the following from your training run:

### Metrics to Record

- **Total categories classified** (should be 2,024)
- **Confidence distribution (baseline):** count of HIGH, MEDIUM, LOW
- **Confidence distribution (fine-tuned):** count of HIGH, MEDIUM, LOW
- **Total categories that changed domain** after fine-tuning
- **Mean cosine similarity (baseline):** average across all categories
- **Mean cosine similarity (fine-tuned):** average across all categories
- **Number of manual corrections** used in training
- **Total training examples generated** (printed during Phase 2)
- **Training time** (printed during Phase 3)

### Results to Record

- **Per-domain category counts** — how many categories landed in each vertical, before and after
- **Per-domain accuracy** — for corrected categories, what percentage the model gets right
- **Top 10 biggest score improvements** — categories that moved the most
- **Top 10 remaining LOW confidence** — categories still uncertain after training

### Failure Cases to Record

- **Suffix poisoning examples** — at least 5 categories where the suffix caused misclassification
- **Cross-domain leakage** — categories that sit at the boundary between two plausible verticals
- **Persistent failures** — categories that remain wrong even after fine-tuning (and why)

---

## Figures Section

### Figure 1 — Confidence Distribution (`figures/confidence_dist.png`)

**Paper section:** Results

**What it proves:** Fine-tuning shifts the score distribution rightward, converting MEDIUM and LOW confidence assignments into HIGH confidence ones. The reduction in the left tail demonstrates that contrastive training resolves ambiguous cases.

**Recommended caption:**
> *Figure 1. Distribution of cosine similarity scores before (red) and after (green) contrastive fine-tuning. Vertical dashed lines indicate the HIGH confidence threshold (0.75) and MEDIUM threshold (0.60). Fine-tuning produces a significant rightward shift, reducing the number of uncertain classifications from N₁ to N₂.*

### Figure 2 — Per-Domain Accuracy (`figures/per_domain_accuracy.png`)

**Paper section:** Results

**What it proves:** Accuracy improvements are not uniform across verticals — domains that suffered most from suffix poisoning (Industrial, Education) show the largest gains, while domains with distinctive vocabulary (Healthcare, Automotive) were already accurate at baseline.

**Recommended caption:**
> *Figure 2. Classification accuracy per sales vertical before (red) and after (green) contrastive fine-tuning, evaluated against manually verified ground truth. Verticals most affected by suffix poisoning (Industrial, Education, Professional) show the greatest accuracy gains.*

### Figure 3 — t-SNE Embedding Space (`figures/tsne_baseline.png` and `figures/tsne_finetuned.png`)

**Paper section:** Results / Discussion

**What it proves:** The baseline embedding space shows significant cluster overlap between verticals that share suffix vocabulary ("station", "company", "supplier"). After fine-tuning, clusters tighten and domain anchor points (stars) move to the center of their respective clusters, demonstrating that the model has internalized the taxonomy structure.

**Recommended caption (baseline):**
> *Figure 3a. t-SNE projection of category embeddings from the base e5-base-v2 model. Colors indicate assigned vertical. Significant overlap is visible between Industrial (purple), Professional (blue), and Education (cyan) clusters, caused by shared suffix vocabulary.*

**Recommended caption (fine-tuned):**
> *Figure 3b. t-SNE projection after contrastive fine-tuning. Cluster separation has improved substantially. Domain anchor points (stars) now sit near their cluster centroids, indicating successful taxonomy internalization.*

### Figure 4 — Suffix Poisoning Analysis (`figures/suffix_analysis.png`)

**Paper section:** Methodology / Problem Formulation

**What it proves:** Certain suffixes ("supplier", "station", "company") appear in hundreds of categories and consistently produce lower cosine similarity scores in baseline results. This quantifies the suffix poisoning phenomenon and motivates the need for fine-tuning.

**Recommended caption:**
> *Figure 4. Suffix poisoning analysis. Left: frequency of categories ending in each suffix. Right: mean baseline cosine similarity per suffix group. High-frequency suffixes ("service", "supplier", "station") correlate with lower classification confidence, confirming that generic English suffixes degrade semantic alignment in taxonomy routing.*

---

## Tables Section

### Table 1 — Dataset Statistics

| Statistic | Value |
|---|---|
| Total business categories | *(fill: e.g. 2,024)* |
| Master sales verticals | *(fill: e.g. 11 + ARCHIVE)* |
| Avg. categories per vertical | *(fill: total / 11)* |
| Domain description length (avg. words) | *(fill: count from domains.py)* |
| Manual corrections provided | *(fill: len(MANUAL_CORRECTIONS))* |
| Training examples generated | *(fill: printed in Phase 2)* |
| Embedding dimensionality | 768 |

### Table 2 — Suffix Poisoning Summary

| Suffix | Category Count | Mean Baseline Score | Most Common Wrong Vertical | Example Category |
|---|---|---|---|---|
| station | *(fill)* | *(fill)* | *(fill: e.g. V10_Education)* | `power station` |
| company | *(fill)* | *(fill)* | *(fill: e.g. V5_Industrial)* | `software company` |
| supplier | *(fill)* | *(fill)* | *(fill: e.g. V5_Industrial)* | `beauty product supplier` |
| service | *(fill)* | *(fill)* | *(fill)* | *(fill)* |
| center | *(fill)* | *(fill)* | *(fill)* | *(fill)* |
| contractor | *(fill)* | *(fill)* | *(fill)* | *(fill)* |

### Table 3 — Model Configuration

| Parameter | Value |
|---|---|
| Base model | `intfloat/e5-base-v2` |
| Architecture | 12-layer Transformer (110M params) |
| Embedding dimension | 768 |
| Loss function | CosineSimilarityLoss |
| Batch size | 16 |
| Epochs | 4 |
| Warmup steps | 10 |
| Learning rate | 2e-5 (default) |
| Query prefix | `query:` |
| Passage prefix | `passage:` |
| HIGH threshold | 0.75 |
| MEDIUM threshold | 0.60 |

---

## Paper Structure

### Recommended Section Order

1. **Abstract** (~200 words)
   - State the problem: aligning unstructured business categories to a controlled sales taxonomy
   - Name the failure mode: suffix poisoning
   - Name the method: anchor description contrastive fine-tuning
   - State the result: X% of categories classified with HIGH confidence after training, up from Y%

2. **Introduction** (~500 words)
   - Business context: why sales teams need category-to-vertical mapping
   - Scale of the problem: 2,000+ categories, 11 verticals, manual mapping is impractical
   - Key insight: general-purpose embeddings fail because of suffix poisoning
   - Contribution summary: a lightweight fine-tuning method that requires only ~30 manual corrections

3. **Related Work**
   - Sentence embeddings: SBERT, E5, Instructor
   - Taxonomy alignment: ontology matching, schema alignment
   - Few-shot classification: prompt-based, contrastive learning, SetFit
   - Distinguish your work: you're fine-tuning on anchor descriptions, not labeled examples

4. **Methodology**
   - Problem formulation: given C categories and D domain descriptions, find f: C → D
   - Suffix poisoning analysis (use Figure 4 here)
   - Anchor description contrastive fine-tuning: positive/negative pair construction
   - Training signal: manual corrections + high-confidence anchors

5. **Experiments**
   - Dataset statistics (Table 1)
   - Model configuration (Table 3)
   - Evaluation protocol: confidence thresholds, ground truth from corrections

6. **Results**
   - Confidence distribution shift (Figure 1)
   - Per-domain accuracy (Figure 2)
   - Embedding space visualization (Figure 3a, 3b)
   - Suffix poisoning resolution (Table 2)

7. **Discussion**
   - Why it works: contrastive loss reshapes the embedding space around domain anchors
   - Limitations: requires domain descriptions, corrections are manual, may not generalize to unseen taxonomies
   - Scalability: adding new verticals requires retraining; adding new categories does not

8. **Conclusion**
   - Restate the contribution
   - Practical impact: zero-cost runtime classification via dictionary lookup
   - Future work: automated correction mining, multi-level taxonomy support

---

## What the Baseline Results Prove

Frame the baseline results as **motivation** for your method:

> "We evaluate the zero-shot classification capability of e5-base-v2, a state-of-the-art sentence embedding model, on the task of controlled vocabulary taxonomy alignment. Despite strong performance on standard retrieval benchmarks, the model achieves HIGH confidence (cosine similarity > 0.75) on only **X%** of categories. Analysis reveals that **suffix poisoning** — where generic English suffixes such as 'station', 'supplier', and 'company' dominate the semantic signal — systematically misdirects categories to semantically adjacent but taxonomically incorrect verticals."

Key talking points:
- The model is not "bad" — it correctly understands English semantics
- The failure is specific to **taxonomy alignment** where business context matters more than surface-level word meaning
- The failure is **systematic**, not random — it follows predictable suffix patterns

---

## What the Fine-tuned Results Prove

Frame the fine-tuned results as your **contribution**:

> "After contrastive fine-tuning with only **N manual corrections**, HIGH confidence classifications increase from X% to Y%, and domain assignment accuracy on corrected categories improves from A% to B%. The t-SNE visualization confirms that the embedding space reorganizes around domain anchor points, resolving the cluster overlap caused by suffix poisoning."

Key talking points:
- The improvement is achieved with **minimal human effort** (~30 corrections out of 2,000 categories)
- The method preserves what the model already gets right (high-confidence anchors prevent forgetting)
- The final artifact is a **static dictionary** — no model needed at inference time for known categories
- The trained model generalizes to **unseen categories** without additional corrections

---

## How to Name Your Contribution

### The Failure Mode

> **Suffix Poisoning in Controlled Vocabulary Taxonomy Alignment**

Definition: The systematic misclassification of taxonomy entries caused by generic English suffixes (e.g., "station", "supplier", "company") that dominate the embedding signal in sentence-level models, overriding the domain-specific semantic content of the entry.

### The Method

> **Anchor Description Contrastive Fine-tuning (ADCF)**

Definition: A lightweight fine-tuning strategy that reshapes a pre-trained sentence embedding space by contrasting short taxonomy entries against rich natural-language domain anchor descriptions, using cosine similarity loss with manually verified positive and negative pairs augmented by high-confidence zero-shot anchors.

---

## BibTeX Citations

### sentence-transformers (SBERT)

```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title     = {Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks},
    author    = {Reimers, Nils and Gurevych, Iryna},
    booktitle = {Proceedings of the 2019 Conference on Empirical Methods
                 in Natural Language Processing and the 9th International
                 Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
    year      = {2019},
    pages     = {3982--3992},
    publisher = {Association for Computational Linguistics},
    url       = {https://arxiv.org/abs/1908.10084},
}
```

### E5 Embedding Model (intfloat/e5-base-v2)

```bibtex
@article{wang2022text,
    title   = {Text Embeddings by Weakly-Supervised Contrastive Pre-training},
    author  = {Wang, Liang and Yang, Nan and Huang, Xiaolong and Jiao, Binxing
               and Yang, Linjun and Jiang, Daxin and Majumder, Rangan and Wei, Furu},
    journal = {arXiv preprint arXiv:2212.03533},
    year    = {2022},
    url     = {https://arxiv.org/abs/2212.03533},
}
```

### t-SNE

```bibtex
@article{van2008visualizing,
    title   = {Visualizing Data using t-SNE},
    author  = {van der Maaten, Laurens and Hinton, Geoffrey},
    journal = {Journal of Machine Learning Research},
    volume  = {9},
    number  = {86},
    pages   = {2579--2605},
    year    = {2008},
    url     = {https://jmlr.org/papers/v9/vandermaaten08a.html},
}
```

### scikit-learn

```bibtex
@article{pedregosa2011scikit,
    title   = {Scikit-learn: Machine Learning in Python},
    author  = {Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
               and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
               and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A.
               and Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
    journal = {Journal of Machine Learning Research},
    volume  = {12},
    pages   = {2825--2830},
    year    = {2011},
    url     = {https://jmlr.org/papers/v12/pedregosa11a.html},
}
```
