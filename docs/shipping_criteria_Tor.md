# Model Shipping Criteria — KKU'3S Sentiment Analysis


---

## 1. Purpose

These criteria define how the team will determine whether a candidate sentiment model is suitable for deployment on the KKU'3S platform.

The criteria are derived from the business values defined in the **KKU'3S Business Requirement Document**. All models will be evaluated on the same TweetEval test set.

---

## 2. Ready-to-Ship Criteria

### Criterion 1 — Overall Sentiment Performance

**Derived from:**  
Seller Reputation Quantification + User Experience Improvement

**Requirement:**  
The model should perform well across **negative, neutral, and positive** sentiment classes without being dominated by the majority class.

**Primary Metric:** Macro F1

**Calculation:**

$$
F1_c = \frac{2 \times Precision_c \times Recall_c}
{Precision_c + Recall_c}
$$

$$
Macro\ F1 =
\frac{F1_{negative}+F1_{neutral}+F1_{positive}}{3}
$$

**Why:**  
The TweetEval test set is class-imbalanced. Macro F1 gives equal importance to all sentiment classes, making it more appropriate than accuracy for evaluating balanced sentiment performance.

**Shipping expectation:**  
A candidate should achieve a Macro F1 that is competitive with or better than the baseline.

---

### Criterion 2 — Negative Detection & Robustness

**Derived from:**  
Content Risk Control + Seller Reputation Quantification + User Experience Improvement

**Requirement:**  
The model should reliably detect negative feedback while maintaining stable performance across different types of user-generated text.

#### 2.1 Negative Sentiment Detection

**Primary Metric:** Negative Recall

**Calculation:**

$$
Negative\ Recall =
\frac{TP_{negative}}
{TP_{negative}+FN_{negative}}
$$

**Why:**  
For Content Risk Control, missing an actual negative comment may prevent potentially problematic content from being identified.

---

#### 2.2 Robustness Across Text Characteristics

**Metrics:**

- Macro F1
- Negative Recall

Performance will be evaluated across relevant data slices:

| Metadata | Slices |
|---|---|
| Text Length | Short / Long |
| Emoji | Emoji / No Emoji |
| Hashtag | Hashtag / No Hashtag |
| Mention | Mention / No Mention |

**Why:**  
User-generated content can vary in length and structure. A model should not achieve strong overall performance while failing on a specific type of text.

**Shipping expectation:**  
The candidate should not show severe performance degradation on important data slices compared with its overall performance and the baseline.

---

### Criterion 3 — Prediction Reliability

**Derived from:**  
Content Risk Control + Platform Content Management

**Requirement:**  
The model should provide confidence information that can support automated processing and human review.

**Metrics:**

- Confidence Score
- Calibration analysis / Expected Calibration Error (ECE), if applicable

**Why:**  
Low-confidence predictions can be escalated to platform administrators instead of being handled automatically.

**Operational Rule:**

```text
Prediction
    ↓
Confidence Score
    ↓
 ┌───────────────────┐
 │ High Confidence   │ → Automated Handling
 └───────────────────┘
          │
          │ Low Confidence
          ↓
 ┌───────────────────┐
 │ Human Review      │
 └───────────────────┘