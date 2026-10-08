# Model Shipping Criteria — KKU’3S Sentiment Analysis

## 1. Purpose and business requirements

The sentiment subsystem helps administrators review negative feedback and summarize user sentiment on the KKU’3S platform. It predicts **negative, neutral and positive** sentiment. A negative prediction may highlight a complaint about poor service or suspected fraud, but it does not establish that fraud occurred or identify who is responsible.

The criteria below connect model performance to the business goals named in the earlier criteria document: **Seller Reputation Quantification, User Experience Improvement, Content Risk Control and Platform Content Management**. These are proposed links between those goals and the evaluation metrics, rather than independently verified acceptance requirements from the business requirement document.

We use **baseline as the reference for the three-class task**. Candidates must be evaluated on the same test examples, labels and protocol. The requirements are relative to baseline rather than arbitrary absolute score thresholds.

## 2. Criteria summary

| Criterion | Business connection and purpose | Reference-based requirement |
| --- | --- | --- |
| **1. Macro F1** | **Seller Reputation Quantification + User Experience Improvement:** assess balanced classification of negative, neutral and positive feedback. | Prefer Macro F1 at least as high as baseline. Inspect per-class F1 so a weak class is not hidden by the average. |
| **2. Negative recall** | **Content Risk Control + User Experience Improvement:** reduce missed negative feedback that may contain complaints about poor service or suspected fraud. | Prefer negative recall at least as high as baseline. Inspect missed-negative counts and recall in negation and contrast groups. |
| **3. Negative precision** | **Seller Reputation Quantification + Platform Content Management:** reduce incorrect negative flags, unnecessary review and the risk of unfair action against users. | Prefer negative precision at least as high as baseline. Any decrease must be explained together with the benefit in recall and the extra false alerts. |
| **4. Metadata checks** | **User Experience Improvement + Content Risk Control:** check whether the model handles different types of user text consistently. | Compare Macro F1, negative recall and negative precision against baseline within every evaluated group. Explain regressions and report group/class support. |

## 3. How the metrics are calculated and why they matter

### Criterion 1 — Balanced sentiment performance: Macro F1

**Requirement:** The model should distinguish all three sentiment classes well, including the less frequent classes.

For each class $c$, evaluate that class against all other classes:

$$
Precision_c = \frac{TP_c}{TP_c + FP_c}, \qquad
Recall_c = \frac{TP_c}{TP_c + FN_c}
$$

$$
F1_c = \frac{2\times Precision_c\times Recall_c}{Precision_c + Recall_c}
$$

$$
Macro\ F1 = \frac{F1_{negative}+F1_{neutral}+F1_{positive}}{3}
$$

**Business connection:** A sentiment summary used to support reputation assessment should reflect positive and negative feedback while also recognizing neutral comments. Macro F1 gives every class equal weight. This is useful for the imbalanced TweetEval test set, where accuracy can be strongly influenced by the largest class.

**Decision:** Prefer Macro F1 at least as high as baseline and inspect each class separately. A lower Macro F1 requires an explicit benefit in the intended use; a small difference alone does not establish a reliable advantage.

### Criterion 2 — Finding negative feedback: Negative recall

For negative sentiment:

- **TP:** an actual negative text correctly predicted as negative.
- **FN:** an actual negative text predicted as neutral or positive.

$$
Negative\ Recall = \frac{TP_{negative}}{TP_{negative}+FN_{negative}}
$$

**Interpretation:** Of all actual negative messages, how many does the model find? For example, finding 80 out of 100 actual negatives gives 80% recall and leaves 20 missed messages. This is an illustration, not a shipping threshold.

**Business connection:** Missing negative feedback may prevent administrators from noticing poor service, dissatisfaction or a complaint about suspected fraud. Higher recall supports Content Risk Control by helping surface these messages for review. It measures negative sentiment detection, not fraud detection accuracy.

**Decision:** Prefer recall at least as high as baseline. Report the number of missed negatives and check recall in the negation and contrast groups. Read recall together with precision: predicting more texts as negative may increase recall while also increasing false alerts.

### Criterion 3 — Limiting incorrect flags: Negative precision

For negative sentiment:

- **TP:** an actual negative text correctly predicted as negative.
- **FP:** an actual neutral or positive text incorrectly predicted as negative.

$$
Negative\ Precision = \frac{TP_{negative}}{TP_{negative}+FP_{negative}}
$$

**Interpretation:** Of all messages flagged as negative, how many are actually negative? For example, if 70 of 100 negative flags are correct, precision is 70% and 30 flags are false alerts. This is an illustration, not a shipping threshold.

**Business connection:** Incorrect negative flags can distort sentiment summaries and increase administrator workload. If used in reputation assessment or moderation, they could also contribute to unfair treatment of a seller or service provider. Better precision reduces this risk, although even a correctly identified negative text does not prove misconduct.

**Decision:** Prefer precision at least as high as baseline. If a candidate increases recall but lowers precision, report both the reduction in missed negatives and the additional false alerts before justifying the replacement. A sentiment flag should lead to text review rather than an automatic accusation or penalty.

### Criterion 4 — Robustness across metadata groups

Metadata is used to divide the test set into evaluation groups; it is not added as a model input feature in this evaluation.

| Metadata in FINAL_RUN | Groups | What to inspect |
| --- | --- | --- |
| Text length | Short / medium / long | Whether brief or longer feedback creates more errors. |
| Emoji | Present / absent | Whether emoji-containing texts are handled differently. |
| Negation | Present / absent | Whether patterns such as “not good” cause missed negative feedback. |
| Contrast | Present / absent | Whether words such as “but” occur in texts with conflicting sentiment cues. |
| Capitalization | None / low / high uppercase ratio | Whether capitalization patterns are associated with different errors. |
| Repeated letters | Present / absent | Whether informal spelling such as “baaad” is handled differently. |

**Business connection:** User feedback varies in length and writing style. Strong overall performance can hide weaknesses in a group important to users. Negation and contrast are proposed priorities because they can change how feedback should be interpreted; their prevalence and importance in actual KKU’3S traffic still need confirmation.

**Decision:** Explain improvements and regressions across all six metadata features. A model does not need to win every group to be preferred, but important regressions require justification. Small groups provide limited evidence. If no text is predicted negative, precision is undefined; if there are no actual negatives, recall is undefined. Mark these cases unavailable rather than treating them as a reliable score.

Groups can overlap. Do not add their error counts or average their scores into a replacement overall metric. Keyword or emoji presence is not itself a sentiment label.

## 4. Model selection and release decision

**Straightforward replacement:** Match or exceed baseline on Macro F1, negative recall and negative precision, with an improvement in at least one. Review per-class results and metadata regressions before accepting the replacement.

**Trade-off decision:** If core metrics move in opposite directions, explain the changes in missed negatives, false alerts and relevant groups. Justify the choice using the intended use and the team's priorities. The criteria do not automatically accept that exchange. **Baseline is the preferred model for future integration; BERTweet is the preferred new candidate and production alternative.** Neither new candidate dominates baseline on all three core metrics. This is a benchmark-based preference, not proof of production readiness or statistically significant superiority. Baseline is the comparison reference, not the existing production version.

**Production comparison:** Production has only negative/positive outputs. Compare it with candidates only under the same PN protocol, after verifying its label mapping and tokenizer compatibility. Do not compare its PN score directly with native three-class scores.

**Before release:** These benchmark criteria support model selection. Improving on baseline does not by itself establish that a model is suitable for deployment. Confirm performance on representative KKU’3S feedback, including the intended language(s), and retain human review before approving release.

## 5. Integration and recovery

After representative-data validation, integrate the preferred model using the same tokenizer, preprocessing, native label mapping and length limit as the final notebook. Return sentiment and confidence for administrator review. Monitor negative false alerts/missed negatives, neutral recall, metadata groups, latency and inference failures. Retain a versioned previous configuration for rollback if quality or service degrades. Actual deployment and rollback have not been implemented in this project evaluation.

Evidence: [final notebook](../FINAL_RUN.ipynb) and [metrics conclusion](metrics_conclusion.md). Historical notebooks are retained under [history_sources](history_sources/).
