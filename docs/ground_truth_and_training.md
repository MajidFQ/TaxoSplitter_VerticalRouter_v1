# Ground Truth & Embedding Training Strategy

This document outlines the methodology behind creating the "Ground Truth" taxonomy dataset and the subsequent strategy for fine-tuning the embedding model. By migrating away from an unsupervised, zero-shot approach toward a supervised, LLM-generated baseline, we guarantee deterministic accuracy while preventing embedding collapse.

---

## 1. How We Create the Ground Truth

We utilize a **Large Language Model (GPT-OSS 120B)** as an automated data labeler to map our 2,000+ raw business categories into 14 precise, business-model-aligned domains (plus an `ARCHIVE` bucket).

### The Methodology
1. **Rule-Based Definitions:** Instead of generic descriptions (e.g., "places that sell food"), each of the 14 domains is defined by a strict `RULE` anchored in economic reality. For example, `D03_Automotive` is defined strictly as: *"The business sells, repairs, services, rents, or cleans motor vehicles or vehicle-specific parts and accessories."*
2. **Compact System Prompting:** Sending massive context windows to an LLM dilutes its attention. Our script (`groq_labeler.py`) dynamically extracts only the core `RULE` for each domain. This creates a hyper-dense, ~750-token system prompt that forces the LLM to make logical, policy-based routing decisions rather than relying on loose semantic vibes.
3. **Deterministic Batching:** Categories are sent in batches of 15. The model runs with `temperature=0.0` to eliminate hallucination. Every response is validated structurally; if the JSON is malformed or a hallucinated domain key is returned, the script automatically catches it and retries.

### Why This is Highly Accurate
- **Semantic Independence:** Zero-shot cosine similarity suffers from "suffix poisoning" (e.g., classifying a "power station" as "Education" because "station" is semantically close to "police station"). An LLM with 120 billion parameters understands the *functional definition* of a power plant and routes it to `D13_Manufacturing` based on the rule.
- **Explicit Exclusions:** The domain rules were engineered with explicit edge-case guardrails. The LLM knows that a veterinarian is `D02_PetCare`, not `D01_Healthcare`, because the `D01` rule explicitly demands a "human patient".

---

## 2. Training the Embedding Model

Once `outputs/ground_truth.json` is generated, it serves as the absolute source of truth for the final pipeline step: fine-tuning `intfloat/e5-base-v2`.

### The Goal of Fine-Tuning
The goal is **not** to make the model memorize the 2,000 categories. The goal is to mathematically warp the embedding space so that the model internalizes our 14 domain boundaries. This ensures that when the model encounters a **completely new, unseen category** in production, it places it in the correct semantic bucket.

### Preventing Overfitting and Model Collapse
Previously, the model suffered from "training collapse" (assigning >0.99 cosine similarity to incorrect domains) because contradictory manual corrections were confusing the gradient loss. With a pristine, 2,000-item ground truth, we apply the following safety measures:

#### 1. Contrastive Loss (CosineSimilarityLoss)
We do not train the model to output text. We train it to push related vectors together (Label = `1.0`) and pull unrelated vectors apart (Label = `0.0`). 
- **Positive Pairs:** `("pizza restaurant", "D07_FoodDining") -> 1.0`
- **Negative Pairs:** `("pizza restaurant", "D03_Automotive") -> 0.0`

#### 2. Hard Negative Mining
To make the model truly robust, we deliberately train it on its own mistakes. If the base model thinks "police station" and "power station" are similar, we explicitly feed that pair to the loss function with a `0.0` label. This teaches the model to ignore the "station" suffix and focus on the core noun.

#### 3. Low Epochs, Low Learning Rate
Embedding models are notoriously fragile. Over-training destroys the rich, pre-trained semantic knowledge of the model (Catastrophic Forgetting).
- **Learning Rate:** `2e-5` (Very slow, gentle updates).
- **Epochs:** `2` (We only pass through the data twice).
- **Warmup Steps:** 10% of the training time is spent slowly ramping up the learning rate to prevent initial shock to the weights.

#### 4. The Anchor Signal Dominance
Because the LLM labeled *every* category, we have ~2,000 positive pairs and ~26,000 negative pairs. This massive, consistent signal creates a strong gravitational pull for each domain. A few edge-case anomalies won't derail the training because the sheer volume of correct, consistent data (the "Anchor Signal") keeps the vector space stable.

### The Production Pipeline
In production, the pipeline operates in `O(1)` time:
1. When a category arrives, we first check the static `ground_truth.json` lookup table.
2. If it's a direct hit, routing is instant and 100% accurate.
3. If it's a novel/unseen category, the newly fine-tuned model embeds it and calculates cosine similarity against the 14 domain definitions. Because the model's spatial geometry has been corrected, it will naturally route the novel category into the correct bucket without falling for suffix traps.
