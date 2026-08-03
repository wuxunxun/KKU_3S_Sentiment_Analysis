# Business Requirement Document - KKU'3S
**Document Version**: V0.1
**Last Updated Date**: 2026-07-30
**Editor**: Wu Xun, Yahyaa, Tor
**Status**: *In Progress*


## Part 1: Project Overview 
### 1.1 Project Background

This sentiment analysis subsystem is an AI pre-development module customized for the **KKU'3S 2nd-hand trading platform**.

KKU'3S is a campus exclusive second-hand goods trading platform designed for students, teachers, and shop owners of Khon Kaen University, covering core business modules including commodity publishing, online bargaining, idle item transaction, and user comment interaction. **3S** represents **Seek, Share and Swap**.

Massive user comments, commodity reviews and post texts will be generated during platform operation. To automatically judge user emotional tendency (positive / negative feedback), analyze merchant reputation and monitor public opinion risks, an NLP(Natural Language Processing) sentiment analysis system is required as the essential AI capability of the whole platform.

### 1.2 Project Purpose & Objectives
1. **Academic Objective**: Complete course assessment requirements; Adopt two designated models assigned by the course: **twitter-roBERTa-base**, **gpt2-finetuning-sentiment-model-3000-samples**, together with optional candidate models. Conduct inference and testing based on the TweetEval sentiment dataset respectively. Compare overall accuracy, F1 score, inference efficiency and anti-interference ability against noisy tweets among all involved models, select the optimal one to be deployed as the official sentiment analysis module for the KKU'3S campus second-hand trading platform.

2. **Technical Objective**: Build standardized project engineering architecture, proficiently use **Hugging Face** toolkit and **Weights & Biases** for experiment recording.

3. **Delivery Objective**: Deliver fully runnable source code, complete sets of requirement documents, experimental logs saved in W&B, and final multi-model comparison analysis report.

### 1.3 Related Definitions
1. **Project Name:** KKU'3S, Full name: Khon Kaen University Student Second-hand Swap System.
2. **Project Team Members:** Wu Xun, Yahyaa, Tor (Team roles and personal responsibilities will be supplemented in subsequent revisions).
3. **Customer / Purchasing Party:** Administrative Department of Khon Kaen University, platform operation administrators.
4. **End Users:** All teachers and students enrolled in Khon Kaen University, certified campus merchants, on-campus housing landlords.
5. **Target Market Segment:** Campus idle commodity trading market, a subdivision of localized campus e-commerce.


## Part 2: Business Values Overview 
1. **Content Risk Control**
Automatically identify negative complaints, abusive remarks and inappropriate posts published by users on the platform, assist platform administrators to quickly carry out content review and risk disposal, maintain a healthy campus trading atmosphere.

2. **Seller Reputation Quantification**
Calculate the overall emotional score of all commodity reviews under each seller, convert scattered comment texts into intuitive reputation data.

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