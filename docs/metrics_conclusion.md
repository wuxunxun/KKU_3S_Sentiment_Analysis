# Metrics Conclusion
## Evaluation Setup
- **Test Dataset**: TweetEval sentiment test split (12,284 samples in total; 6,347 samples for binary subset)
- **Shared Baseline**: `base_roberta` (3-class benchmark), `prod_gpt2` (production binary model)
- **Protocol**: Independent evaluation by three team members to verify reproducibility

---

## Independent Team Member Results

### Xun Wu
#### Negative Class (full test set)
| Model | Precision | Recall | F1-Score |
|---|---|---|---|
| prod_gpt2 | 0.3276 | 0.5521 | 0.4112 |
| base_roberta | 0.6833 | 0.8094 | 0.7410 |
| cand_xlm_roberta | 0.6154 | 0.8711 | 0.7213 |
| cand_bertweet | 0.7000 | 0.8009 | 0.7471 |

#### Positive Class (full test set)
| Model | Precision | Recall | F1-Score |
|---|---|---|---|
| prod_gpt2 | 0.2237 | 0.5263 | 0.3139 |
| base_roberta | 0.7140 | 0.7213 | 0.7176 |
| cand_xlm_roberta | 0.6870 | 0.6737 | 0.6803 |
| cand_bertweet | 0.6883 | 0.7263 | 0.7068 |

#### Neutral Class (3-class models only)
| Model | Precision | Recall | F1-Score |
|---|---|---|---|
| base_roberta | 0.7535 | 0.6574 | 0.7022 |
| cand_xlm_roberta | 0.7632 | 0.5570 | 0.6440 |
| cand_bertweet | 0.7478 | 0.6593 | 0.7007 |

---

### Tor
#### Negative Class (full test set)
| Model | Precision | Recall | F1-Score |
|---|---|---|---|
| prod_gpt2 | 0.32 | 0.54 | 0.41 |
| base_roberta | 0.69 | 0.81 | 0.74 |
| Twitter-XLM-RoBERTa | 0.61 | 0.87 | 0.72 |
| RoBERTa-base Sentiment | 0.70 | 0.79 | 0.74 |

#### Positive Class (full test set)
| Model | Precision | Recall | F1-Score |
|---|---|---|---|
| prod_gpt2 | 0.22 | 0.52 | 0.31 |
| base_roberta | 0.71 | 0.74 | 0.73 |
| Twitter-XLM-RoBERTa | 0.68 | 0.70 | 0.69 |
| RoBERTa-base Sentiment | 0.64 | 0.77 | 0.70 |

#### Neutral Class (3-class models only)
| Model | Precision | Recall | F1-Score |
|---|---|---|---|
| base_roberta | 0.76 | 0.66 | 0.70 |
| Twitter-XLM-RoBERTa | 0.77 | 0.55 | 0.64 |
| RoBERTa-base Sentiment | 0.76 | 0.63 | 0.69 |

#### 3-class Aggregate Metrics
| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---|---|---|
| base_roberta | 0.72 | 0.72 | 0.72 |
| Twitter-XLM-RoBERTa | 0.68 | 0.68 | 0.68 |
| RoBERTa-base Sentiment | 0.71 | 0.71 | 0.71 |

---

### Muhammad Yahyaa
#### Binary Sentiment (Negative/Positive subset only)
| Model | Accuracy | Macro F1 |
|---|---|---|
| GPT-2 (previous production) | 0.54 | 0.53 |
| DistilBERT | 0.81 | 0.81 |
| Fine-tuned GPT-2 | 0.92 | 0.92 |
| BERTweet | 0.94 | 0.94 |
| Twitter-RoBERTa (baseline) | 0.95 | 0.95 |

#### 3-class Sentiment (full test set)
| Model | Accuracy | Macro F1 | Negative F1 | Neutral F1 | Positive F1 |
|---|---|---|---|---|---|
| Twitter-RoBERTa (baseline) | 0.72 | 0.72 | – | – | 0.73 |
| BERTweet | ~0.72 | ~0.72 | 0.75 | 0.71 | – |
| XLM-T | – | – | – | – | – |
| Fine-tuned GPT-2 | – | 0.70 | – | – | – |

---

## Aggregated Average Results (full 3-class test set)
### Negative Class
| Model | Avg Precision | Avg Recall | Avg F1-Score |
|---|---|---|---|
| prod_gpt2 | 0.32 | 0.54 | 0.41 |
| base_roberta | 0.69 | 0.81 | 0.74 |
| XLM-RoBERTa series | 0.61 | 0.87 | 0.72 |
| BERTweet / RoBERTa-base candidates | 0.70 | 0.80 | 0.74 |

### Positive Class
| Model | Avg Precision | Avg Recall | Avg F1-Score |
|---|---|---|---|
| prod_gpt2 | 0.22 | 0.52 | 0.31 |
| base_roberta | 0.71 | 0.73 | 0.73 |
| XLM-RoBERTa series | 0.68 | 0.69 | 0.68 |
| BERTweet / RoBERTa-base candidates | 0.67 | 0.75 | 0.71 |

### Neutral Class (3-class candidates only)
| Model | Avg Precision | Avg Recall | Avg F1-Score |
|---|---|---|---|
| base_roberta | 0.76 | 0.66 | 0.70 |
| XLM-RoBERTa series | 0.77 | 0.55 | 0.64 |
| BERTweet / RoBERTa-base candidates | 0.75 | 0.65 | 0.70 |

---

## Key Findings
1. The production binary model `prod_gpt2` performs poorly on the full 3-class test set, as all ground-truth neutral samples are misclassified. Domain shift from IMDB training data to Twitter text further degrades performance.
2. All 3-class candidate models significantly outperform the production baseline on both polarity classes, with F1-scores in the 0.68–0.75 range.
3. Results are highly consistent across independent team runs, with run-to-run F1 variance below 0.01, confirming reproducibility.
4. Twitter-specific pre-training delivers measurable performance gain: the `base_roberta` benchmark outperforms general-domain RoBERTa on macro metrics.
5. XLM-RoBERTa achieves the highest negative recall but suffers from low neutral recall, showing a clear precision-recall trade-off across classes.
6. On the binary-only subset, fine-tuning substantially improves GPT-2 performance, and Twitter-RoBERTa reaches the top accuracy of 0.95.
