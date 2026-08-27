# KKU'3S Sentiment Analysis Project

**Course:** CP388 302 — Software Development and Project Management for Data Science and Artificial Intelligence  
**Project:** KKU'3S Sentiment Analysis  
**Milestone:** Milestone #1  
**Team Members:** Wu Xun, Muhammad Yahyaa, Tor  
**Status:** In Progress

---

## Project Introduction

This is a group course project supporting the **KKU'3S campus second-hand trading platform**.

KKU'3S stands for **Seek, Share, and Swap**. It is designed as a campus-exclusive second-hand trading platform for the Khon Kaen University community, supporting activities such as item publishing, item search, online negotiation, transaction processing, user comments, reviews, and platform content management.

The sentiment analysis subsystem is intended to identify emotional tendencies in user-generated text using three sentiment classes:

- **Negative**
- **Neutral**
- **Positive**

The project evaluates multiple sentiment classification models using the **TweetEval** benchmark, compares their behavior and performance, and determines whether a candidate model should replace the current on-production model for future integration into the KKU'3S platform.


For more details, see the [Business Requirement Document](docs/business_requirement.md).


---

## Milestone #1 Objectives

Milestone #1 focuses on understanding the problem, defining evaluation criteria, exploring the dataset, and preparing the model-selection process.

The team is expected to:

1. Define product features, targeted customers, end users, and market segment.
2. Decide on the proposed **Ready-to-Ship** criteria.
3. Explore the **TweetEval** benchmark dataset and the assigned Hugging Face sentiment models.
4. Perform EDA, statistical analysis, data cleansing, and data preparation as needed.
5. Choose candidate models and explain the model-selection rationale.
6. Define the metrics used to measure and monitor model performance.
7. Set up **Weights & Biases (W&B)** and the team GitHub repository.

---

## Identified Issues

### Label space mismatch between production baseline and benchmark

`prod_gpt2` is a binary classification model with no neutral class. It cannot be directly compared with the 3-class benchmark dataset and the other 3-class models on the full test set. Direct full-dataset evaluation is methodologically unfair and invalid.

All selected models are evaluated on the same test set to keep the comparison consistent and reproducible.

### Selected Solution

1. All models are evaluated exclusively on the Negative / Positive subset as the unified primary benchmark, using binary F1-score as the core ranking metric for fair head-to-head comparison.
2. Adopt a two-tier evaluation framework:
   - **Primary ranking**: Binary performance of all 4 models, used as the core basis for model selection.
   - **Supplementary analysis**: 3-class full-set metrics (neutral-class performance, macro-F1) are calculated separately for the three 3-class models, to demonstrate extended capability beyond the current production version.

---

## EDA and Data Preparation

The current workflow includes:

- Inspecting TweetEval train, validation, and test splits.
- Checking sentiment label distributions.
- Examining class imbalance.
- Reviewing tweet length and text characteristics.
- Preparing model-compatible tokenization.
- Normalizing Twitter-specific text patterns when required.
- Inspecting class-level behavior and misclassification patterns.


### Current EDA Visualization

![TweetEval Sentiment Overview](asset/images/eda_sentiment_overview.png)

---

## Model Evaluation Strategy

All team members share `base_roberta` as the 3-class benchmark and `prod_gpt2` as the current production baseline. Each member selected independent candidate models covering multilingual, lightweight and domain-adaptation scenarios.

| Role | Model Type | Representative Models |
|---|---|---|
| Benchmark | 3-class Twitter-optimized | `base_roberta` |
| Production | Binary GPT-2 | `prod_gpt2` |
| Candidates | 3-class Twitter-optimized | `XLM-RoBERTa`, `BERTweet`, `DistilBERT`, `fine-tuned GPT-2` |


For model-selection details, see [Model Selection](docs/model_selection.md).

---

## Evaluation Metrics

All models are evaluated on the TweetEval test set across three independent team runs.

### 3-Class Test Set (12,284 samples)
| Model Group | Negative F1 | Neutral F1 | Positive F1 | Key Note |
| --- | --- | --- | --- | --- |
| Production binary model (`prod_gpt2`) | 0.41 | — | 0.31 | Limited by missing neutral class and IMDB-to-Twitter domain mismatch |
| All 3-class candidates | 0.68 – 0.75 | 0.64 – 0.70 | 0.68 – 0.73 | Significantly outperform the production baseline |
| Best balanced (BERTweet / Twitter-RoBERTa) | ~0.74 | ~0.70 | ~0.72 | Twitter-specific pre-training delivers consistent performance gain |

### Binary Subset (Negative / Positive only)
| Rank | Top Model | Accuracy | Macro F1 |
| --- | --- | --- | --- |
| 1 | Twitter-RoBERTa | 0.95 | 0.95 |

For detailed metric conclusion, see [Metrics Definition](docs/metrics_conclusion.md).

---

## Proposed Ready-to-Ship Criteria

For the **3-class sentiment detection model**, the current proposed minimum threshold is:

- **Accuracy >= 70%**
- **Macro Recall >= 70%**
- **Macro F1-Score >= 70%**

Macro F1 remains the primary metric. These thresholds are preliminary and should be finalized after team discussion, baseline comparison, slice analysis, and further validation.

For more details, see [Model Shipping Criteria](docs/shipping_criteria.md).

---

## Team Collaboration

This project is developed collaboratively by:

- **Xun Wu**
- **Muhammad Yahyaa**
- **Tor**

| Notebook | Team Member |
|---|---|
| `milestone1_MuhammadYahyaa.ipynb` | Muhammad Yahyaa |
| `milestone1_TOR.ipynb` | Tor |
| `milestone1_XUNWU.ipynb` | Xun Wu |


---
