# Shipping Criteria Overview
Applicable Client: Browser Web

Scope: Release criteria for sentiment analysis model, chat content safety monitoring and user behavior risk prediction.


## 1. Module Release Acceptance Criteria (Primary Metrics for Current Phase)
### 1.1 Metrics for Sentiment Module
- **Sentiment detection model** (3-class: Positive / Neutral / Negative): Accuracy ≥ ____%, Recall ≥ ____%, F1 ≥ ____%

- Additional model metrics for hate & offensive content (*Not in current scope, reserved for reference)
    - Hate Detection: Accuracy ≥ ____%, Recall ≥ ____%, F1 ≥ ____%
    - Offensive Detection: Accuracy ≥ ____%, Recall ≥ ____%, F1 ≥ ____%
    - Irony Detection: Accuracy ≥ ____%, Recall ≥ ____%, F1 ≥ ____%

- Detection quantitative indicators (*Not in current scope, reserved for reference)
    - Detection rate of explicit violating text ≥ ____%
    - Detection rate of homophones, split characters and variant implicit violating content ≥ ____%
    - False positive rate of normal friendly conversations misjudged as violation ≤ ____%

### 1.2 Chat / Post / Comment Content Safety Monitoring Standard
(Insulting, defamatory, obscene and harmful remarks)
Monitoring Scope: Personal insult, malicious defamation and attack, vulgar pornographic content, malicious provocative remarks.

> **2.1 Enforcement Policy**
> 1. Confirmed high-risk violation: Directly block output, remind user of content violation and retain records
> 2. Borderline suspicious content: Mark risk, store records in backend for manual review without direct blocking
>
> **2.2 Test Cases**
> 1. Direct abusive language and personal attack text
> 2. Sarcastic and implied defamatory statements
> 3. Vulgar and explicit obscene expressions
> 4. Violating content that users try to bypass detection with symbols or homophones *(Extra supporting capability required)*

### 1.3 General Function, Performance & Compatibility Release Criteria
(*Not in current scope, reserved for reference)
To be supplemented later