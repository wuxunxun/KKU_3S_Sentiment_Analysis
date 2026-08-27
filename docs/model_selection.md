# Model Selection
## Standard Label Schema (Project Unified)
All model outputs are aligned to the following 3-class schema for consistent cross-model comparison.
| Standard ID | Sentiment Class |
|---|---|
| 0 | Negative |
| 1 | Neutral |
| 2 | Positive |

---

## Common Baseline & Production Models
Shared by all team members as the evaluation reference.

### base_roberta (Benchmark)
- **Hugging Face ID**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Native Label Space**: 3-class
- **Official Summary**: RoBERTa base model fine-tuned on 58M English tweets, optimized for short informal social media text.
- **Label Mapping (Native → Standard)**:
  - `LABEL_0` → 0 (Negative)
  - `LABEL_1` → 1 (Neutral)
  - `LABEL_2` → 2 (Positive)

### prod_gpt2 (Current Production)
- **Hugging Face ID**: `LYTinn/gpt2-finetuning-sentiment-model-300-samples`
- **Native Label Space**: Binary (no Neutral class)
- **Official Summary**: GPT-2 fine-tuned on IMDB movie reviews for binary sentiment polarity classification.
- **Label Mapping (Native → Standard)**:
  - `0` → 0 (Negative)
  - `1` → 2 (Positive)
  - No native output for Neutral (class 1)

---

## Candidate Models by Team Member

### Xun Wu
#### cand_xlm_roberta
- **Hugging Face ID**: `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Native Label Space**: 3-class (multilingual)
- **Official Summary**: Multilingual XLM-RoBERTa classifier fine-tuned on cross-lingual Twitter sentiment corpora.
- **Selection Rationale**: Introduces native multilingual support for the KKU'3S platform's future international student expansion.
- **Label Mapping (Native → Standard)**:
  - `LABEL_0` → 0 (Negative)
  - `LABEL_1` → 1 (Neutral)
  - `LABEL_2` → 2 (Positive)

#### cand_bertweet
- **Hugging Face ID**: `finiteautomata/bertweet-base-sentiment-analysis`
- **Native Label Space**: 3-class
- **Official Summary**: BERT model pre-trained exclusively on English tweets, with custom tokenization for mentions, hashtags and emojis.
- **Selection Rationale**: Optimized for short social text, matching the comment and review format of the second-hand trading platform.
- **Label Mapping (Native → Standard)**:
  - `LABEL_0` → 0 (Negative)
  - `LABEL_1` → 1 (Neutral)
  - `LABEL_2` → 2 (Positive)

---

### Tor
#### Twitter-XLM-RoBERTa
- **Hugging Face ID**: `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Native Label Space**: 3-class (multilingual)
- **Official Summary**: Cross-lingual sentiment model based on XLM-RoBERTa architecture, trained on multilingual Twitter data.
- **Selection Rationale**: Evaluates multilingual capability and cross-lingual generalization for diverse campus users.
- **Label Mapping (Native → Standard)**:
  - `LABEL_0` → 0 (Negative)
  - `LABEL_1` → 1 (Neutral)
  - `LABEL_2` → 2 (Positive)

#### RoBERTa-base Sentiment
- **Hugging Face ID**: General-domain fine-tuned `roberta-base`
- **Native Label Space**: 3-class
- **Official Summary**: Standard RoBERTa base model fine-tuned on general-domain sentiment benchmarks.
- **Selection Rationale**: Serves as a domain-adaptation reference to quantify performance gain from Twitter-specific pre-training.
- **Label Mapping (Native → Standard)**:
  - `0` → 0 (Negative)
  - `1` → 1 (Neutral)
  - `2` → 2 (Positive)

---

### Muhammad Yahyaa
#### DistilBERT Sentiment
- **Hugging Face ID**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Native Label Space**: Binary
- **Official Summary**: Lightweight distilled BERT model optimized for fast inference with reduced parameters.
- **Selection Rationale**: Explores lightweight deployment options with lower latency and compute cost for production.
- **Label Mapping (Native → Standard)**:
  - `0` → 0 (Negative)
  - `1` → 2 (Positive)
  - No native output for Neutral (class 1)

#### Fine-tuned GPT-2 (Extended)
- **Hugging Face ID**: `LYTinn/gpt2-finetuning-sentiment-model-300-samples` (extended tuning)
- **Native Label Space**: Binary
- **Official Summary**: GPT-2 model further fine-tuned with expanded sentiment training samples.
- **Selection Rationale**: Measures the performance ceiling of the existing GPT-2 production architecture with additional tuning.
- **Label Mapping (Native → Standard)**:
  - `0` → 0 (Negative)
  - `1` → 2 (Positive)
  - No native output for Neutral (class 1)
