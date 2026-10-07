# KKU'3S Sentiment Analysis

**Course:** CP388 302 — Software Development and Project Management for Data Science and Artificial Intelligence  
**Project:** KKU'3S Sentiment Analysis  
**Team Members:** Wu Xun, Muhammad Yahyaa, Tor  
**Status:** Final Submission

---

## 1. Project Overview

KKU'3S (Seek, Share, and Swap) is a campus-exclusive second-hand trading platform for the Khon Kaen University community.

This project develops and evaluates a sentiment analysis module to classify user-generated text into three sentiment classes:

- **Negative**
- **Neutral**
- **Positive**

The objective is to evaluate several sentiment classification models, analyze their performance across different textual characteristics, and select a preferred model for the next validation stage of the KKU'3S platform.

---

## 2. Project Objectives

The project aims to:

1. Evaluate sentiment classification models for the KKU'3S use case.
2. Compare candidate models against the current reference baseline.
3. Evaluate model performance using accuracy, Macro F1, and per-class metrics.
4. Analyze model behavior across different textual characteristics.
5. Select a preferred model based on the evaluation results.
6. Organize the final experimental results for reproducibility.

---

## 3. Dataset

The project uses the **TweetEval sentiment** dataset.

The dataset contains three sentiment classes:

| Label | Sentiment |
|---:|---|
| 0 | Negative |
| 1 | Neutral |
| 2 | Positive |

### Dataset Splits

| Split | Samples |
|---|---:|
| Train | 45,615 |
| Validation | 2,000 |
| Test | 12,284 |

The final evaluation uses all **12,284 English TweetEval test samples**:

- Negative: 3,972
- Neutral: 5,937
- Positive: 2,375

The test set is imbalanced, with Neutral as the largest class. Therefore, Macro F1 and per-class metrics are considered alongside accuracy.

---

## 4. Models

Four models were evaluated:

| Role | Model |
|---|---|
| Baseline | `cardiffnlp/twitter-roberta-base-sentiment-latest` |
| Current Production | `LYTinn/gpt2-finetuning-sentiment-model-3000-samples` |
| Candidate 1 | `finiteautomata/bertweet-base-sentiment-analysis` |
| Candidate 2 | `cardiffnlp/twitter-xlm-roberta-base-sentiment` |

The Baseline, BERTweet, and XLM-R models support native three-class sentiment classification.

The Production GPT-2 model is binary and does not support the Neutral class. Therefore, it is evaluated separately using a Positive/Negative (PN) protocol.

---

## 5. Data Preparation

Before model inference, the test dataset was checked for:

- Missing texts
- Missing labels
- Empty texts
- Duplicate texts
- Duplicate sample IDs
- Invalid labels

All data-quality checks passed, and all 12,284 test samples were retained.

Model-specific preprocessing and tokenization were applied during inference. Metadata was extracted from the original text and was used only for analysis, not as model input.

Inference settings:

- Batch size: 16
- Maximum sequence length: 128 tokens
- GPU acceleration when available

---

## 6. Metadata Analysis

Six metadata features were extracted from the original text to analyze model performance across different textual characteristics.

| Metadata | Definition |
|---|---|
| `has_emoji` | Indicates whether the text contains at least one emoji. |
| `text_length_bin` | Categorizes text as Short, Medium, or Long based on word-count quantiles. |
| `has_contrast` | Indicates whether the text contains contrast words such as `but`, `however`, `although`, `though`, or `yet`. |
| `has_negation` | Indicates whether the text contains negation words or expressions such as `not`, `never`, `no`, `don't`, `can't`, and related forms. |
| `uppercase_ratio` | Ratio of uppercase alphabetic letters to all alphabetic letters. |
| `has_repeated_chars` | Indicates whether the same letter appears at least three consecutive times. |

### Metadata Grouping

Text length is divided using the one-third and two-thirds quantiles of word counts in the test dataset:

- **Short:** word count ≤ 12
- **Medium:** 12 < word count ≤ 18
- **Long:** word count > 18

These thresholds are derived from the word-count distribution of the test dataset.

For `uppercase_ratio`, an initial threshold of **30%** was considered. However, this resulted in a highly imbalanced distribution:

| Category | Count | Percentage |
|---|---:|---:|
| None | 622 | 5.06% |
| Low | 11,166 | 90.89% |
| High | 496 | 4.04% |

Because most samples were classified as Low, the threshold was adjusted to **10%** to provide a more informative distribution for slice analysis.

With the 10% threshold:

| Category | Count | Percentage |
|---|---:|---:|
| None | 622 | 5.06% |
| Low | 7,428 | 60.47% |
| High | 4,234 | 34.47% |

The final grouping is:

- **None:** `uppercase_ratio = 0`
- **Low:** `0 < uppercase_ratio ≤ 10%`
- **High:** `uppercase_ratio > 10%`

The 10% threshold reduces the severe imbalance observed with the initial 30% threshold and provides a more informative basis for comparing model performance across uppercase-related text characteristics.

Metadata groups are used for slice analysis only and are not supplied to the models as input features.

---

## 7. Evaluation Strategy

Two evaluation protocols are used.

### Native Three-Class Evaluation

The Baseline, BERTweet, and XLM-R models are evaluated on all 12,284 test samples using their native three-class predictions.

Metrics include:

- Accuracy
- Macro Precision
- Macro Recall
- Macro F1
- Per-class Precision
- Per-class Recall
- Per-class F1

### Positive/Negative (PN) Evaluation

A separate PN evaluation excludes true Neutral samples and uses the remaining **6,347 Negative/Positive samples**.

For the three-class models, the predicted class is selected between Negative and Positive based on their predicted probabilities.

The PN results are supplementary and should not be directly compared with the native three-class results.

---

## 8. Final Results

### Native Three-Class Evaluation

| Model | Accuracy (%) | Macro Precision (%) | Macro Recall (%) | Macro F1 (%) | Negative Precision (%) | Negative Recall (%) |
|---|---:|---:|---:|---:|---:|---:|
| **Baseline** | **72.18** | **71.87** | 73.49 | **72.40** | 68.95 | 80.66 |
| BERTweet | 72.02 | 71.33 | **73.64** | 72.19 | **70.47** | 80.21 |
| XLM-R | 68.19 | 68.93 | 70.61 | 68.42 | 61.50 | **86.93** |

The Baseline achieved the highest Accuracy and Macro F1 among the evaluated three-class models.

BERTweet achieved the highest Negative Precision, while XLM-R achieved the highest Negative Recall.

---

## 9. Per-Class Performance

| Model | Class | Precision (%) | Recall (%) | F1 (%) |
|---|---|---:|---:|---:|
| Baseline | Negative | 68.95 | 80.66 | 74.35 |
| Baseline | Neutral | 75.66 | 65.76 | 70.36 |
| Baseline | Positive | 71.01 | 74.06 | 72.51 |
| BERTweet | Negative | 70.47 | 80.21 | **75.03** |
| BERTweet | Neutral | 75.39 | 65.10 | 69.87 |
| BERTweet | Positive | 68.13 | 75.62 | 71.68 |
| XLM-R | Negative | 61.50 | **86.93** | 72.04 |
| XLM-R | Neutral | **77.05** | 54.96 | 64.16 |
| XLM-R | Positive | 68.24 | 69.94 | 69.08 |

BERTweet achieves the highest Negative F1, while XLM-R achieves the highest Negative Recall. However, XLM-R has substantially lower Negative Precision and overall Macro F1.

---

## 10. Metadata Findings

Metadata slice analysis provides additional information about model behavior across different text characteristics.

### Negation

For texts containing negation:

| Model | Macro F1 | Negative Recall |
|---|---:|---:|
| Baseline | 67.92% | 86.94% |
| BERTweet | 67.35% | 83.60% |
| XLM-R | 59.80% | 91.36% |

XLM-R achieves the highest Negative Recall for texts containing negation, but its Macro F1 is substantially lower.

### Contrast

For texts containing contrast words:

| Model | Macro F1 | Negative Recall |
|---|---:|---:|
| Baseline | 69.27% | 83.50% |
| BERTweet | **69.74%** | 79.80% |
| XLM-R | 62.20% | **88.22%** |

BERTweet achieves slightly higher Macro F1 than the Baseline, while XLM-R achieves the highest Negative Recall.

### Text Length

For short texts:

| Model | Macro F1 | Negative Precision | Negative Recall |
|---|---:|---:|---:|
| Baseline | 71.56% | 59.45% | 75.00% |
| BERTweet | 71.55% | **60.97%** | **76.49%** |
| XLM-R | 67.40% | 49.38% | 82.34% |

BERTweet provides slightly higher Negative Precision and Negative Recall than the Baseline for short texts, although their Macro F1 values are almost identical.

### Repeated Characters

The `has_repeated_chars = True` group contains only **132 samples**. BERTweet achieves a Macro F1 of 74.43%, compared with 73.48% for the Baseline.

Because of the relatively small sample size, this result should be interpreted cautiously.

### Emoji and Uppercase

Performance differences for emoji and uppercase groups vary between the models. These metadata slices are used to identify potential differences in model behavior, but they do not by themselves determine the final model selection.

Metadata groups may overlap, so each slice is analyzed independently.

---

## 11. Model Selection

The model selection considers:

1. **Macro F1**
2. **Negative Recall**
3. **Negative Precision**
4. **Metadata slice performance**

The Baseline is used as the reference model.

### Performance Change from Baseline

| Model | Accuracy Change | Macro F1 Change | Negative Precision Change | Negative Recall Change |
|---|---:|---:|---:|---:|
| Baseline | 0.00 pp | 0.00 pp | 0.00 pp | 0.00 pp |
| BERTweet | -0.16 pp | -0.21 pp | **+1.52 pp** | -0.45 pp |
| XLM-R | -3.99 pp | -3.98 pp | -7.45 pp | **+6.27 pp** |

### Final Model Decision

**Twitter-RoBERTa Baseline is retained as the preferred model for the next validation stage.**

The Baseline achieves the highest overall Accuracy and Macro F1.

BERTweet is a close alternative, providing higher Negative Precision and slightly better performance on some metadata slices, particularly short texts. However, its overall Macro F1 and Negative Recall are slightly lower than the Baseline.

XLM-R achieves substantially higher Negative Recall, but this comes with a considerable reduction in Negative Precision and overall Macro F1.

Therefore, the available evaluation results do not provide sufficient evidence to replace the Baseline.

---

## 12. Production Model Comparison

The Production GPT-2 model is evaluated separately using the PN protocol because it does not support the Neutral class.

| Model | Accuracy (%) | Macro F1 (%) | Negative Precision (%) | Negative Recall (%) |
|---|---:|---:|---:|---:|
| **Baseline** | **94.64** | **94.30** | 96.09 | 95.32 |
| BERTweet | 94.60 | 94.29 | **97.17** | 94.11 |
| XLM-R | 92.63 | 92.08 | 93.39 | 94.94 |
| Production GPT-2 | 53.60 | 52.61 | 65.59 | 54.38 |

The Production GPT-2 model uses a provisional label mapping and does not support the Neutral class. Therefore, its results are treated separately and should not be directly compared with the native three-class results.

The PN results also show that the Baseline and BERTweet perform very similarly, while the Production GPT-2 model performs substantially lower under this evaluation protocol.

---

## 13. Error Analysis

The error analysis identified several patterns:

- **Neutral boundaries:** Models may classify Neutral texts as Positive or Negative, or classify Positive/Negative texts as Neutral.
- **High-confidence errors:** High prediction confidence does not guarantee a correct prediction.
- **Context and ambiguity:** Some texts may require additional contextual information to determine sentiment accurately.
- **Production limitations:** Errors from the Production GPT-2 model should be interpreted carefully because its label mapping is provisional and it does not support the Neutral class.

Five randomly selected prediction errors per model were inspected for qualitative analysis. These examples are intended for qualitative inspection and do not represent the frequency of each error type.

---

## 14. Experiment Tracking

Weights & Biases (W&B) is used to record:

- Model configurations
- Predictions
- Confidence scores
- Evaluation metrics
- Metadata slice results
- Prediction error examples
- Final evaluation files

The final evaluation outputs are stored in:

```text
results/final_run/
```

---

## 15. Reproducibility

The main final workflow is provided in:

```text
FINAL_RUN_With_Conclusion.ipynb
```

The notebook performs the following steps:

1. Load and verify the TweetEval sentiment dataset.
2. Check the quality of the test data.
3. Extract six metadata features.
4. Verify model labels and mappings.
5. Run inference for the evaluated models.
6. Calculate native three-class metrics.
7. Calculate the Positive/Negative metrics.
8. Perform metadata slice analysis.
9. Analyze prediction errors.
10. Record experiment results using Weights & Biases.
11. Save the final evaluation results to `results/final_run/`.

The final workflow was executed using GPU acceleration when available.

---

## 16. Limitations

- TweetEval contains English Twitter data and may not fully represent actual KKU'3S user feedback.
- The Production GPT-2 model uses a provisional label mapping.
- The Production GPT-2 model does not support the Neutral class.
- Metadata features are used for analysis and are not model inputs.
- Some metadata groups have limited sample support, particularly repeated-character texts.
- The uppercase ratio threshold was adjusted based on the distribution of the test dataset and is intended for slice analysis rather than model input.
- No paired statistical significance test was performed.
- Benchmark performance alone does not establish deployment readiness.

Further validation using representative KKU'3S data is required before production deployment.

---

## 17. Conclusion

The final evaluation shows that the **Twitter-RoBERTa Baseline** provides the strongest overall performance among the evaluated three-class sentiment models.

The Baseline achieved the highest:

- **Accuracy: 72.18%**
- **Macro F1: 72.40%**

BERTweet is a close alternative, with higher Negative Precision and the highest Negative F1. It also shows slightly better performance than the Baseline for some metadata slices, particularly short texts.

XLM-R achieves the highest Negative Recall at **86.93%**, but its Negative Precision and overall Macro F1 are substantially lower than the Baseline.

Therefore, the project **retains the Twitter-RoBERTa Baseline as the preferred model for the next validation stage**.

This decision is based on the TweetEval benchmark and should not be interpreted as final deployment approval. Further validation using representative KKU'3S data and the intended application context is required before production deployment.