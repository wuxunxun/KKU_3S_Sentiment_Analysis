# Model Selection — KKU’3S Sentiment Analysis

## 1. Final experiment and model roles

The final experiment follows the two-new-candidate option. No model training or production improvement is claimed. Milestone #1 experiments are retained in [history_sources](history_sources/) as background. The canonical workflow is [FINAL_RUN.ipynb](../FINAL_RUN.ipynb).

| Role | Model ID | Native labels |
|---|---|---|
| Baseline / reference | `cardiffnlp/twitter-roberta-base-sentiment-latest` | 0: negative; 1: neutral; 2: positive |
| Current production / replacement target | `LYTinn/gpt2-finetuning-sentiment-model-3000-samples` | 0: LABEL_0; 1: LABEL_1 |
| New candidate 1 | `finiteautomata/bertweet-base-sentiment-analysis` | 0: NEG; 1: NEU; 2: POS |
| New candidate 2 | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | 0: negative; 1: neutral; 2: positive |

Production's semantic mapping, 0 = negative and 1 = positive, is provisional, based on IMDb label definitions rather than explicit author confirmation. Its repository tokenizer/model compatibility remains unresolved. Native class IDs are mapped to semantic labels per model; production has no neutral output.

## 2. Candidate rationale

**BERTweet:** evaluates a Twitter-oriented model with its own normalization/tokenization pipeline, relevant to short and informal feedback. The recorded test results show competitive overall performance and fewer negative false alerts than baseline.

**XLM-R:** introduces a multilingual model family rather than a second closely related monolingual RoBERTa checkpoint. This experiment tests English sentiment only; multilingual or Thai deployment quality is not established by these results.

The selection draws on the team's earlier experiments. Historical DistilBERT, other RoBERTa and fine-tuning experiments are not part of the final four-model comparison.

## 3. Evaluation protocols

- **Native three-class:** baseline and both new candidates use native predictions on the same 12,284 samples.
- **Production native PN:** evaluate production on the 6,347 samples with true negative/positive labels; true neutral samples are excluded.
- **Adapted PN comparison:** use that same subset for all four models. Three-class models choose between negative and positive probabilities, ignoring neutral. This is supplementary adapted decoding, not native three-class behavior or an official replacement for the full task.

PN and three-class scores must not be mixed into a single ranking. Metadata is calculated from original text and never supplied as an additional model input.

## 4. Final preference

**Preferred model for future production integration: Twitter-RoBERTa baseline. Preferred new candidate and production alternative: BERTweet.** Baseline remains a reference model; selecting it does not make it a new candidate or imply it was the current production model.

| Native three-class measure | Baseline | BERTweet | XLM-R |
|---|---:|---:|---:|
| Accuracy (%) | 72.18 | 72.02 | 68.19 |
| Macro F1 (%) | 72.40 | 72.19 | 68.42 |
| Negative precision (%) | 68.95 | 70.47 | 61.50 |
| Negative recall (%) | 80.66 | 80.21 | 86.93 |

Baseline has the highest observed overall Macro F1 and higher negative recall than BERTweet in the negation and contrast groups. BERTweet is the most balanced of the two new candidates, reduces false alerts by 108 relative to baseline, and improves short-text negative precision and recall. XLM-R finds more negatives but produces substantially more false alerts and has weaker neutral recognition. Small baseline–BERTweet differences do not establish statistical superiority.

The recorded results support this preference, not unconditional release approval. Validate quality, latency and cost on representative KKU’3S feedback before deployment. Production's low recorded PN score must be interpreted with its unresolved configuration limitations.

## 5. Future work

If time and cost permit, explore baseline and BERTweet jointly, with an additional decision module for disagreements. This is not implemented and does not guarantee improvement. A learned module requires separate training and validation data; the current test set must not train it.

## 6. Evidence

- [Overall and metadata analysis](metrics_conclusion.md)
- [Shipping criteria](shipping_criteria.md)
- [Saved results](../results/final_run/)
- [Recorded W&B run](https://wandb.ai/xun-w-khon-kaen-university/KKU3S-Sentiment-M1/runs/ntpb8rb2) (team access)
- Model cards: [baseline](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest), [production](https://huggingface.co/LYTinn/gpt2-finetuning-sentiment-model-3000-samples), [BERTweet](https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis), [XLM-R](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment).
