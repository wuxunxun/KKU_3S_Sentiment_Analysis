# Business Requirement Document

## Part 1: Project Overview 
### 1.1 Project Background

This sentiment analysis subsystem is an AI pre-development module customized for the **KKU'3S 2nd-hand trading platform**.

KKU'3S is a campus exclusive second-hand goods trading platform designed for students, teachers, shop owner, etc of Khon Kaen University, covering commodity publishing, online bargaining, idle item transaction, user comment interaction core business modules. **3S** represents **Seek, Share and Swap**.

Massive user comments, commodity reviews and post texts will be generated during platform operation. To automatically judge user emotional tendency (positive / negative feedback), analyze merchant reputation and monitor public opinion risks, an NLP(Natural Language Processing) sentiment analysis system is required as the essential AI capability of the whole platform.

### 1.2 Project Purpose & Objectives

1. **Academic Objective**: Complete course assessment requirements; Adopt two designated models assigned by the course: **twitter-roBERTa-base**、**gpt2-finetuning-sentiment-model-3000-samples** and **optional models** finish training and testing based on the TweetEval sentiment dataset respectively. Compare overall accuracy, F1 score, training speed, inference efficiency and anti-interference ability against noisy tweets among all involved models, select the optimal one to be deployed as the official sentiment analysis module for the KKU'3S campus second-hand trading platform.
2. **Technical Objective**: Build simple project engineering architecture, proficiently use **Hugging Face** toolkit and **Weights & Biases** for experiment recording.
3. **Delivery Objective**: Deliver fully runnable source code, complete sets of requirement documents, complete experimental logs saved in W&B, and final multi-model comparison analysis report.

### 1.3: Related Definitions

1. **Project Name:** KKU'3S, Full name: Khon Kaen University Student Second-hand Swap System.
2. **Project Team Members:** Wu Xun, Yahyaa, Tor(Team roles, personal responsibilities will be supplemented and perfected in the follow-up revision).
3. **Customer / Purchasing Party:** Administrative Department of Khon Kaen University, platform operation administrators, etc.
4. **End Users:** All teachers and students enrolled in Khon Kaen University, certified campus merchants, housing landlords inside the university.
5. **Target Market Segment:** Campus idle commodity trading market, belonging to the subdivision field of localized campus e-commerce.


## Part 2: Business Values Overview 

1. **Content Risk Control**
Automatically identify negative complaints, abusive remarks and inappropriate posts published by users on the platform, assist platform administrators to quickly carry out content review and risk disposal, maintain a healthy campus trading atmosphere.

2. **Seller Reputation Quantification**
Calculate the overall emotional score of all commodity reviews under each seller, convert scattered comment texts into intuitive reputation data.

3. **User Experience Improvement**
Collect aggregated user emotional feedback for platform trading rules, commodity categories and service experience, provide data basis for the iterative optimization of KKU'3S platform functions.


## Part 3: Team Criteria for Model Shipment & Reasoning
