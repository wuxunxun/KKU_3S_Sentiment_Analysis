# Metrics Conclusion — KKU’3S Sentiment Analysis

## 1. Evaluation setup and scope

This conclusion uses the recorded results of the current four-model evaluation. 


| Role | Model ID | Native outputs |
| --- | --- | --- |
| Baseline | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Negative / neutral / positive |
| Production | `LYTinn/gpt2-finetuning-sentiment-model-3000-samples` | Negative / positive; mapping provisional |
| Candidate | `finiteautomata/bertweet-base-sentiment-analysis` | Negative / neutral / positive |
| Candidate | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Negative / neutral / positive |

| Protocol | Examples | True class support | Eligible models |
| --- | --- | --- | --- |
| A. Native three-class | 12,284 | Negative 3,972; neutral 5,937; positive 2,375 | Baseline, BERTweet, XLM-R |
| B. Shared PN | 6,347 | Negative 3,972; positive 2,375 | All four models |

**Protocol A:** Use each three-class model’s native prediction on the full test set. Production cannot output neutral, so it is not ranked as a native three-class candidate.

**Protocol B:** Keep only examples whose true label is negative or positive. Every model chooses the larger of `p_negative` and `p_positive`; ties select negative. For three-class models this is adapted decoding: `p_neutral` is ignored. For production it is native binary decoding. The subset is selected by the true label, not the predicted label.

PN scores cannot be compared directly with three-class scores. Both the evaluated examples and the decoding rule change. A high PN score does not demonstrate good neutral handling.

Recorded inference settings: batch size 16, maximum 128 tokens and model-specific preprocessing. Production’s 0/1 label mapping is provisional; its tokenizer/model compatibility needs verification before interpreting replacement benefits as definitive.

## 2. Protocol A — native three-class results

### 2.1 Overall metrics

| Model | Accuracy | Macro F1 | Weighted F1 | Negative precision | Negative recall |
| --- | --- | --- | --- | --- | --- |
| Baseline (Twitter-RoBERTa) | 72.18 | 72.40 | 72.06 | 68.95 | 80.66 |
| BERTweet | 72.02 | 72.19 | 71.89 | 70.47 | 80.21 |
| XLM-R | 68.19 | 68.42 | 67.66 | 61.50 | 86.93 |

**Macro F1:** Baseline has the highest observed value, 72.40%, followed closely by BERTweet at 72.19%. The gap is only 0.21 percentage points and does not establish statistical superiority. XLM-R is 3.98 points below baseline.

**Accuracy and weighted F1:** Both favor baseline slightly over BERTweet. Neutral is the largest class, accounting for 48.33% of the test set, so an always-neutral prediction would already achieve 48.33% accuracy. Macro F1 and per-class scores are therefore useful alongside accuracy.

**Negative precision:** BERTweet is best at 70.47%, 1.52 points above baseline. A larger fraction of its negative flags are correct. XLM-R is 7.45 points below baseline.

**Negative recall:** XLM-R is best at 86.93%, 6.27 points above baseline. BERTweet is 0.45 points below baseline. Higher recall must be assessed together with the extra false alerts.

### 2.2 Per-class results

| Model | Class | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- | --- |
| Baseline (Twitter-RoBERTa) | Negative | 68.95 | 80.66 | 74.35 | 3,972 |
| Baseline (Twitter-RoBERTa) | Neutral | 75.66 | 65.76 | 70.36 | 5,937 |
| Baseline (Twitter-RoBERTa) | Positive | 71.01 | 74.06 | 72.51 | 2,375 |
| BERTweet | Negative | 70.47 | 80.21 | 75.03 | 3,972 |
| BERTweet | Neutral | 75.39 | 65.10 | 69.87 | 5,937 |
| BERTweet | Positive | 68.13 | 75.62 | 71.68 | 2,375 |
| XLM-R | Negative | 61.50 | 86.93 | 72.04 | 3,972 |
| XLM-R | Neutral | 77.05 | 54.96 | 64.16 | 5,937 |
| XLM-R | Positive | 68.24 | 69.94 | 69.08 | 2,375 |

- **Negative:** BERTweet has the best F1 (75.03%), reflecting its precision/recall balance. XLM-R’s higher recall is offset by lower precision.
- **Neutral:** Baseline has the best F1 (70.36%). XLM-R has the highest neutral precision but the lowest neutral recall (54.96%): many actual neutral texts are assigned a polarity.
- **Positive:** Baseline has the best F1 (72.51%). BERTweet finds more positives but makes more incorrect positive predictions, resulting in a lower F1.

### 2.3 Confusion matrices

Rows are true classes; columns are predicted classes. These are recorded native three-class counts.

**Baseline (Twitter-RoBERTa)**

| True / predicted | Negative | Neutral | Positive |
| --- | --- | --- | --- |
| Negative | 3204 | 711 | 57 |
| Neutral | 1372 | 3904 | 661 |
| Positive | 71 | 545 | 1759 |

**BERTweet**

| True / predicted | Negative | Neutral | Positive |
| --- | --- | --- | --- |
| Negative | 3186 | 729 | 57 |
| Neutral | 1289 | 3865 | 783 |
| Positive | 46 | 533 | 1796 |

**XLM-R**

| True / predicted | Negative | Neutral | Positive |
| --- | --- | --- | --- |
| Negative | 3453 | 415 | 104 |
| Neutral | 2005 | 3263 | 669 |
| Positive | 157 | 557 | 1661 |

### 2.4 Negative error burden

| Model | Missed negatives (FN) | False alerts (FP) | Of FP: true neutral | Total negative flags |
| --- | --- | --- | --- | --- |
| Baseline (Twitter-RoBERTa) | 768 | 1443 | 1372 | 4647 |
| BERTweet | 786 | 1335 | 1289 | 4521 |
| XLM-R | 519 | 2162 | 2005 | 5615 |

A false alert (FP) is a non-negative text flagged as negative. A false negative (FN) is an actual negative text missed.

Compared with baseline, BERTweet creates **108 fewer false alerts but misses 18 more negatives**. XLM-R misses **249 fewer negatives but creates 719 more false alerts**. Neutral texts account for most false alerts in all three models. For a platform review workflow, these counts describe the exchange between finding complaints and increasing review workload.

## 3. Protocol B — shared negative/positive results

### 3.1 Overall metrics for all four models

| Model | Accuracy | Macro F1 | Negative precision | Negative recall |
| --- | --- | --- | --- | --- |
| Baseline (Twitter-RoBERTa) | 94.64 | 94.30 | 96.09 | 95.32 |
| Production GPT-2 | 53.60 | 52.61 | 65.59 | 54.38 |
| BERTweet | 94.60 | 94.29 | 97.17 | 94.11 |
| XLM-R | 92.63 | 92.08 | 93.39 | 94.94 |

Baseline and BERTweet are very close: their Macro F1 differs by 0.01 percentage points at the recorded precision. Baseline has higher negative recall, while BERTweet has higher negative precision. XLM-R is behind both on Macro F1, although its negative recall remains high.

Production has 53.60% accuracy and 52.61% Macro F1. An always-negative prediction would achieve 62.58% accuracy on this PN subset because negatives are the majority. This highlights the need to investigate the recorded production result. It does not identify whether the cause is configuration, training domain, model quality or another factor.

Relative to production on this same protocol, baseline improves Macro F1 by 41.69 percentage points, precision by 30.50 points and recall by 40.94 points. The gaps are descriptive and remain subject to the production configuration caveat.

### 3.2 PN per-class metrics and error counts

The following counts for the three-class models are **reconstructed**, not directly exported: each integer TP/FP pair uniquely matches the recorded four-decimal negative precision/recall with supports 3,972/2,375, and also reproduces the recorded accuracy and Macro F1. Production’s TP and correct-positive counts are explicitly printed in FINAL_RUN. Per-class metrics below are calculated from these counts.

| Model | Class | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- | --- |
| Baseline (Twitter-RoBERTa) | Negative | 96.09 | 95.32 | 95.70 | 3972 |
| Baseline (Twitter-RoBERTa) | Positive | 92.27 | 93.52 | 92.89 | 2375 |
| Production GPT-2 | Negative | 65.59 | 54.38 | 59.46 | 3972 |
| Production GPT-2 | Positive | 40.67 | 52.29 | 45.75 | 2375 |
| BERTweet | Negative | 97.17 | 94.11 | 95.61 | 3972 |
| BERTweet | Positive | 90.64 | 95.41 | 92.96 | 2375 |
| XLM-R | Negative | 93.39 | 94.94 | 94.16 | 3972 |
| XLM-R | Positive | 91.29 | 88.76 | 90.01 | 2375 |

| Model | Negative → negative | Negative → positive (FN) | Positive → negative (FP) | Positive → positive |
| --- | --- | --- | --- | --- |
| Baseline (Twitter-RoBERTa) | 3786 | 186 | 154 | 2221 |
| Production GPT-2 | 2160 | 1812 | 1133 | 1242 |
| BERTweet | 3738 | 234 | 109 | 2266 |
| XLM-R | 3771 | 201 | 267 | 2108 |

These PN counts exclude every true-neutral text. Do not substitute them for the native three-class error counts above. Production correctly detects 2,160 of 3,972 negatives and 1,242 of 2,375 positives. Its positive recall is 52.29%.

## 4. Metadata definitions and interpretation

Metadata describes the original text and defines evaluation groups. It was not supplied as an extra model input feature.

| Feature | Groups / rule |
| --- | --- |
| Text length | Whitespace word count: short ≤12; medium 13–18; long ≥19. |
| Emoji | Present / absent, using emoji 0.6.0 demojize. |
| Contrast | Whole words: but, however, although, though, yet. |
| Negation | not, never, no, cannot and the contractions defined in FINAL_RUN; curly apostrophes normalized. |
| Uppercase | Uppercase letters / all letters: none = 0; low >0 to 10%; high >10%. |
| Repeated letters | At least three consecutive identical letters, case-insensitive; digits and underscores excluded. |

A text may belong to several groups. Do not sum errors across overlapping groups or average all slice scores into an overall metric. 

## 5. Protocol A — three-class metadata slices

All 14 groups for each of the three eligible models are shown below (42 model/group results). Each model cell is **Macro F1 / negative precision / negative recall (%)**. Support is **negative / neutral / positive**.

| Group | N | Support: Neg / Neu / Pos | Baseline F1 / P / R | BERTweet F1 / P / R | XLM-R F1 / P / R |
| --- | --- | --- | --- | --- | --- |
| Emoji: False | 11475 | 3785 / 5670 / 2020 | 71.85 / 68.95 / 80.69 | 71.68 / 70.50 / 80.24 | 67.96 / 61.61 / 87.13 |
| Emoji: True | 809 | 187 / 267 / 355 | 72.46 / 68.81 / 80.21 | 72.67 / 69.95 / 79.68 | 67.49 / 59.16 / 82.89 |
| Length: short | 4409 | 872 / 2494 / 1043 | 71.56 / 59.45 / 75.00 | 71.55 / 60.97 / 76.49 | 67.40 / 49.38 / 82.34 |
| Length: medium | 4422 | 1442 / 2159 / 821 | 71.79 / 68.63 / 80.72 | 71.51 / 70.09 / 80.44 | 68.65 / 62.24 / 86.55 |
| Length: long | 3453 | 1658 / 1284 / 511 | 71.21 / 74.88 / 83.59 | 71.19 / 76.69 / 81.97 | 65.03 / 68.97 / 89.69 |
| Contrast: False | 11573 | 3675 / 5629 / 2269 | 72.55 / 68.95 / 80.44 | 72.31 / 70.30 / 80.24 | 68.73 / 61.60 / 86.83 |
| Contrast: True | 711 | 297 / 308 / 106 | 69.27 / 68.89 / 83.50 | 69.74 / 72.70 / 79.80 | 62.20 / 60.23 / 88.22 |
| Negation: False | 10217 | 2954 / 5091 / 2172 | 72.77 / 68.57 / 78.50 | 72.65 / 69.81 / 79.05 | 69.29 / 60.96 / 85.41 |
| Negation: True | 2067 | 1018 / 846 / 203 | 67.92 / 69.96 / 86.94 | 67.35 / 72.36 / 83.60 | 59.80 / 63.01 / 91.36 |
| Uppercase: none | 622 | 244 / 282 / 96 | 71.36 / 70.59 / 83.61 | 71.82 / 75.66 / 82.79 | 67.86 / 65.53 / 86.48 |
| Uppercase: low | 7428 | 2756 / 3312 / 1360 | 72.48 / 69.96 / 82.22 | 72.38 / 71.76 / 81.06 | 67.36 / 63.13 / 88.21 |
| Uppercase: high | 4234 | 972 / 2343 / 919 | 71.61 / 65.59 / 75.51 | 71.20 / 65.73 / 77.16 | 68.86 / 56.24 / 83.44 |
| Repeated letters: False | 12152 | 3923 / 5891 / 2338 | 72.37 / 68.89 / 80.65 | 72.14 / 70.38 / 80.14 | 68.38 / 61.41 / 87.05 |
| Repeated letters: True | 132 | 49 / 46 / 37 | 73.48 / 74.07 / 81.63 | 74.43 / 77.78 / 85.71 | 69.49 / 70.37 / 77.55 |

### Interpretation of all six metadata features

1. **Emoji:** On emoji-present texts, BERTweet’s Macro F1 is slightly higher than baseline (72.67% versus 72.46%), with higher negative precision but slightly lower recall. On emoji-absent texts, baseline has slightly higher Macro F1. XLM-R has higher negative recall in both groups but lower precision and Macro F1. Emoji presence does not identify a clear overall winner.
2. **Length:** On short texts, BERTweet improves both negative precision and recall over baseline (60.97%/76.49% versus 59.45%/75.00%), while their Macro F1 is nearly identical. On medium and long texts, baseline has slightly higher Macro F1 and recall, while BERTweet has higher precision. XLM-R’s short-text precision is only 49.38% despite 82.34% recall. Class prevalence changes with length, so this cannot be attributed to length alone.
3. **Contrast:** On contrast-present texts, BERTweet improves precision and Macro F1, but baseline has higher negative recall (83.50% versus 79.80%). Baseline finds 248/297 negatives, compared with BERTweet’s 237/297. XLM-R reaches 88.22% recall but has 60.23% precision and 62.20% Macro F1. Without contrast, baseline leads Macro F1 slightly; BERTweet still favors precision and XLM-R recall.
4. **Negation:** On negation-present texts, baseline has higher Macro F1 and recall than BERTweet; BERTweet has higher precision. Baseline finds 885/1,018 negatives versus BERTweet’s 851/1,018. XLM-R finds more negatives (91.36% recall), but its precision and Macro F1 are weaker. Baseline’s lower Macro F1 in this group does not imply weaker negative detection: its recall is higher than its overall recall. Without negation, BERTweet slightly improves both negative precision and recall over baseline, but baseline still has slightly higher Macro F1.
5. **Uppercase:** For no-uppercase texts, BERTweet leads Macro F1 and precision while baseline has higher recall. For low-uppercase texts, baseline leads Macro F1/recall and BERTweet precision. For high-uppercase texts, BERTweet improves both precision and recall but has lower Macro F1. XLM-R’s high-uppercase recall is 83.44%, with precision of 56.24%. Capitalization may reflect names or acronyms as well as emphasis.
6. **Repeated letters:** With repeated letters, BERTweet leads all three reported metrics; XLM-R is lower than baseline on all three. This group has only 132 texts and 49 actual negatives, so one negative example changes recall by about 2.04 percentage points. Without repeated letters, the general trade-off returns: baseline has slightly higher Macro F1/recall than BERTweet, BERTweet has higher precision, and XLM-R favors recall.

## 6. Protocol B — PN metadata slices for all four models


| PN group | N | Baseline Macro F1 | Production Macro F1 | BERTweet Macro F1 | XLM-R Macro F1 |
| --- | --- | --- | --- | --- | --- |
| Emoji: absent | 5805 | 94.2 | 52.5 | 94.1 | 91.8 |
| Emoji: present | 542 | 93.4 | 48.8 | 94.5 | 92.1 |
| Contrast: absent | 5944 | 94.4 | 52.9 | 94.5 | 92.2 |
| Contrast: present | 403 | 92.5 | 48.0 | 90.5 | 88.9 |
| Negation: absent | 5126 | 94.5 | 51.7 | 94.6 | 92.4 |
| Negation: present | 1221 | 90.2 | 51.1 | 89.9 | 86.4 |
| Repeated letters: absent | 6261 | 94.3 | 52.6 | 94.3 | 92.1 |
| Repeated letters: present | 86 | 95.3 | 51.1 | 94.1 | 88.2 |
| Length: short | 1915 | 93.8 | 54.4 | 94.4 | 91.3 |
| Length: medium | 2263 | 94.6 | 53.0 | 93.6 | 92.5 |
| Length: long | 2169 | 93.1 | 49.8 | 93.6 | 90.6 |
| Uppercase: none | 340 | 94.6 | 53.2 | 95.0 | 91.1 |
| Uppercase: low | 4116 | 94.1 | 52.4 | 93.8 | 92.0 |
| Uppercase: high | 1891 | 94.2 | 51.6 | 94.6 | 91.7 |

### Interpretation of all six metadata features

1. **Emoji:** BERTweet leads on emoji-present texts, while baseline narrowly leads on emoji-absent texts. Production falls from 52.5% without emoji to 48.8% with emoji. This describes a pattern, not a proven emoji effect.
2. **Contrast:** Baseline leads the contrast-present group (92.5%), ahead of BERTweet (90.5%) and XLM-R (88.9%). All four score lower with contrast than without it. Production reaches only 48.0% in the contrast-present group.
3. **Negation:** All four have lower Macro F1 in the negation-present group. Baseline leads that group at 90.2%, narrowly ahead of BERTweet at 89.9%; XLM-R is at 86.4% and production at 51.1%. This supports attention to negation even when PN overall scores are high.
4. **Repeated letters:** Baseline leads the present group at 95.3%, followed by BERTweet at 94.1%, XLM-R at 88.2% and production at 51.1%. Only 86 PN examples remain (49 negative and 37 positive), so the ranking is uncertain. It differs from the native three-class ranking because both the examples and decoding differ.
5. **Length:** BERTweet leads short and long PN groups; baseline leads medium. Production decreases from 54.4% on short texts to 49.8% on long texts. XLM-R is below baseline and BERTweet in all length groups.
6. **Uppercase:** BERTweet leads none/high uppercase; baseline leads low uppercase. Production stays around 51.6–53.2%, well below the other models. Slice Macro F1 alone cannot tell us whether these differences come from missed negatives or false alerts.

The three alternatives outperform production on every displayed PN slice at the chart’s precision. This is consistent with their stronger overall PN results, subject to the unresolved production configuration. It is not a statement about statistical significance.

## 7. Business interpretation and model preference

| Model | Main strength | Main limitation | Conclusion |
| --- | --- | --- | --- |
| Baseline | Highest observed three-class Macro F1; stronger priority-group negative recall than BERTweet; strong PN results. | More false alerts than BERTweet; weaker short-text negative precision/recall. | Preferred model for the next validation stage. |
| BERTweet | Best overall negative precision; fewer false alerts; strong short-text results and competitive PN performance. | Slightly lower three-class Macro F1 and recall; lower priority-group recall than baseline. | Close alternative if reducing review workload has greater priority. |
| XLM-R | Highest native three-class negative recall. | Many more false alerts, lower neutral recall and weaker Macro F1; PN Macro F1 below baseline/BERTweet. | Suitable for further investigation only if higher negative recall justifies the extra review burden. |
| Production GPT-2 | Serves as the existing binary reference. | No neutral output; weak recorded PN results; provisional mapping and compatibility checks remain. | Investigate its configuration; do not use its PN score as a native three-class benchmark. |

**Against the updated shipping criteria:** Neither BERTweet nor XLM-R matches or improves baseline on all three core metrics simultaneously. BERTweet improves precision but loses some recall and Macro F1; XLM-R improves recall but loses precision and Macro F1. Retaining baseline is therefore consistent with the reference-based rule. Metadata results identify trade-offs rather than requiring a model to win every group.

Macro F1 supports balanced sentiment summaries and reputation assessment. Negative recall helps surface negative feedback for review. Negative precision limits incorrect flags and review workload. Metadata analysis identifies text groups where these goals are less well served. Sentiment classification does not verify fraud, misconduct or the target of a complaint, and should not automatically trigger an accusation or penalty.

**Final recommendation:** Prefer baseline for further validation, retain BERTweet as the closest alternative, and document XLM-R’s recall/false-alert trade-off. The recorded results support a model preference; deployment approval requires representative KKU’3S feedback, intended-language validation and human review.