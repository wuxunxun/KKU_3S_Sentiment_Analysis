# Business Requirement Document - KKU'3S
**Document Version**: V1.0
**Last Updated Date**: 2026-10-08
**Editor**: Wu Xun, Yahyaa, Tor
**Status**: *Final evaluation documented; production deployment not performed*


## Part 1: Project Overview 
### 1.1 Project Background

This sentiment analysis subsystem is an AI pre-development module customized for the **KKU'3S 2nd-hand trading platform**.

KKU'3S is a campus exclusive second-hand goods trading platform designed for students, teachers, and shop owners of Khon Kaen University, covering core business modules including commodity publishing, online bargaining, idle item transaction, and user comment interaction. **3S** represents **Seek, Share and Swap**.

Massive user comments, commodity reviews and post texts will be generated during platform operation. The subsystem classifies user text as negative, neutral or positive to support sentiment summaries and administrator review. Sentiment alone does not establish abuse, fraud or responsibility; automated moderation or reputation penalties are outside this evaluation.

### 1.2 Project Purpose & Objectives
1. **Academic Objective**: Evaluate the assigned baseline and current production model together with two new candidates, BERTweet and XLM-R, using TweetEval sentiment. Compare native three-class performance and a separate adapted PN protocol; inspect per-class results and six metadata features. The final preference is baseline for future integration, with BERTweet as the preferred new candidate and alternative. Inference efficiency, deployment latency and cost are future validation items, not measured outcomes of this evaluation.

2. **Technical Objective**: Build standardized project engineering architecture, proficiently use **Hugging Face** toolkit and **Weights & Biases** for experiment recording.

3. **Delivery Objective**: Deliver fully runnable source code, complete sets of requirement documents, experimental logs saved in W&B, and final multi-model comparison analysis report.

### 1.3 Related Definitions
1. **Project Name:** KKU'3S — Seek, Share and Swap, a campus second-hand trading platform.
2. **Project Team Members:** Wu Xun, Muhammad Yahyaa, Tor.
3. **Customer / Purchasing Party:** Administrative Department of Khon Kaen University, platform operation administrators.
4. **End Users:** All teachers and students enrolled in Khon Kaen University, certified campus merchants, on-campus housing landlords.
5. **Target Market Segment:** Campus idle commodity trading market, a subdivision of localized campus e-commerce.

| Category | Definition |
|---|---|
| **Customer / Purchasing Party** | Administrative Department of Khon Kaen University and platform operation administrators |
| **End Users** | KKU students, teachers, certified campus merchants, and on-campus housing landlords |
| **Target Market Segment** | Campus second-hand / idle commodity trading market |
| **Primary AI Users** | Platform administrators and downstream platform services that consume sentiment predictions |


## Part 2: Business Values Overview 
1. **Content Risk Control**
Surface potentially negative feedback for administrator review. Negative sentiment detection is not a validated detector of abusive language, inappropriate content or fraud; any action requires separate review.

2. **Seller Reputation Quantification**
Provide aggregate sentiment summaries as one possible input to reputation assessment. Sentiment does not establish seller responsibility and must not directly trigger penalties.

3. **User Experience Improvement**
Collect aggregated user emotional feedback regarding platform trading rules, commodity categories and service experience, provide data basis for the iterative optimization of KKU'3S platform functions.


## Part 3: KKU'3S Platform Core System Functions
1. **Commodity Publishing**
Users can publish idle goods information, upload product photos, write descriptions and set expected transaction prices.

2. **Item Browse & Search**
All published second-hand items can be browsed. Users can search target goods by keywords.

3. **Post & Demand Release**
Users can publish public posts to share campus experience, or post purchase demands to look for specific idle items. This function can be split into an independent module when platform scale expands in the future.

4. **Online Negotiation & Chat**
Buyers and sellers can chat online to bargain, confirm item conditions and negotiate transaction arrangements.

5. **Guaranteed Transaction with Fund Escrow**
The platform acts as an intermediary. Buyer funds are held in a school-qualified bank account. Funds will be transferred to the seller only after the buyer confirms receiving the item.

6. **Comment & Review**
After the deal, users can leave comments about goods and trading experience.

7. **Platform Content Management**
Administrators monitor posts and user comments to handle inappropriate content and user complaints.

> Supplementary Note
All comment texts and public post contents are the input data source of our sentiment analysis subsystem.

**Standard Platform Transaction Flow**
1. Seller publishes idle commodity information on the platform.
2. Buyer browses the item and contacts the seller via online chat to negotiate price.
3. Both parties reach an agreement; the buyer pays the payment to the school-certified platform custodial account.
4. The seller delivers the goods and provides delivery information.
5. Buyer receives and inspects the item.
6. Buyer confirms receipt on the platform. The platform transfers the reserved funds to the seller’s account.
7. Both sides can submit transaction comments.

## Part 4: Final evaluation scope

The platform functions above describe intended business context; the course deliverable is the offline sentiment evaluation module, not an implemented marketplace.

- Dataset: 12,284 English TweetEval test texts; true negative/positive subset: 6,347.
- Native three-class models: baseline, BERTweet and XLM-R. Production is binary, with provisional label semantics and unresolved tokenizer compatibility.
- Six metadata features define 14 descriptive groups per model; metadata does not change model inputs.
- Preferred future production model: baseline. Preferred new candidate and alternative: BERTweet.
- Human review remains part of the intended use. Representative KKU’3S data, intended languages, latency and cost require validation before release.
- A dual-model disagreement-resolution module is a possible future extension, not a completed feature.

See [model selection](model_selection.md), [shipping criteria](shipping_criteria.md), [metrics conclusion](metrics_conclusion.md) and the [final notebook](../FINAL_RUN.ipynb).
