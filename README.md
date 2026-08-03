# KKU'3S Sentiment Analysis Project

## Project Introduction
This is a group course project supporting the **KKU'3S campus second-hand trading platform**.

The main purpose is to build a sentiment discrimination module to identify emotional tendencies (positive / neutral / negative) from platform user comments.

We will run inference and test multiple candidate models based on the TweetEval dataset, compare the overall performance of each model, and select the optimal model reserved for later deployment on the KKU'3S platform.

## Core Task List (Milestone #1 Requirements)
1. Thinking about your product’s features, then, define the targeted customers, end-users, and market segment.
2. Decide on the “Ready to Ship” criteria to be used.
3. Explore the TweetEval Benchmark dataset and the assigned HuggingFace sentiment analysis models. Perform EDA and statistical analysis on the dataset as needed.
4. Perform data cleansing and data preparation, as needed.
5. Choose candidate models and explain the model selection rationale; discuss strategies to improve the currently on-production model.
6. Define the metrics used to measure and monitor model performance.
7. Set up Weights and Biases (W&B) and the team’s GitHub repository.

### Tools Adopted
- Hugging Face Library: Data processing and model inference
- Weights & Biases: Record full experimental data and evaluation metrics
- Development Language: Python

## Follow-up Experiment TODO
> 1. Create at least five metadata columns to slice data and analyze model behavior in Weights & Biases.
> 2. Run inference on all models and compute evaluation metrics. Inspect misclassified samples to identify error patterns.
> 3. Log predictions, confidence scores, metadata and other critical information to W&B.
> 4. Visualize the performance of candidate models.
> 5. Compare and evaluate candidate sentiment models to decide whether to replace the existing on-production model.
> 6. Provide justification for the final selected deployment model.