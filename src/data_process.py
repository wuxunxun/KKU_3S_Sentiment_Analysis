import pandas as pd
import re
import matplotlib.pyplot as plt
from datasets import load_dataset
from config import TweetEvalConfig as tec
from config import ProjectConfig as pc
from huggingface_hub import whoami, login
# from transformers import pipeline

# check huggingface login status
# hugging face login token : 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
def check_huggingface_login():
    try:
        user_info = whoami()
        print(f"Logged in as: {user_info['name']}")
        return True
    except Exception:
        print("Not logged in. Starting login process...")
        try:
            login()
            print("Login complete.")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    

# check the dataset structure
def check_dataset_structure(dataset, subset, max_records=10):
    if not isinstance(dataset, dict):
        print("Dataset is not a dictionary.")
        return None

    print(f"\n========== Dataset structure - {subset} ==========")
    print(f"Label names: {dataset['train'].features['label'].names}")
    print(f"Checking structure of the '{subset}' subset...")
    df = pd.DataFrame(dataset[subset])

    print("Dataset columns:", df.columns.tolist())
    print("Total records:", len(df))
    print("\nSample data preview:")
    print(df.head(max_records))
    print("\nLabel distribution:")
    print(df['label'].value_counts())
    return df


# EDA 
def get_data_eda(df: pd.DataFrame, subset: str, save_image: bool = False) -> pd.DataFrame:
    print(f"\n========== EDA Analysis - {subset} ==========")
    df = df.copy()
    df["text_length"] = df["text"].apply(lambda x: len(str(x)))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # label distribution
    label_counts = df["label"].value_counts().sort_index()
    # color for the bars
    color_list = ["#d62728", "#1f77b4", "#2ca02c"]
    bar_plot = axes[0].bar(label_counts.index, label_counts.values, color=color_list)

    # axes[0].bar(label_counts.index, label_counts.values)
    axes[0].set_title(f"{subset} Label Distribution")
    # x
    axes[0].set_xlabel("Label ID")
    axes[0].set_xticks([0,1,2])
    axes[0].legend(bar_plot, ["0: Negative", "1: Neutral", "2: Positive"], loc="upper right")
    # y
    axes[0].set_ylabel("Sample Count")
    # grid
    axes[0].grid(axis="y", linestyle="--", alpha=0.35)
    axes[0].set_axisbelow(True)

    # text length histogram
    axes[1].hist(df["text_length"], bins=30)
    axes[1].set_title(f"{subset} Text Length")
    axes[1].set_xlabel("Character Count")
    axes[1].set_ylabel("Frequency")
    # grid
    axes[1].grid(axis="y", linestyle="--", alpha=0.35)
    axes[1].set_axisbelow(True)

    plt.tight_layout()
    if save_image:
        fig_path = pc.IMAGE_DIR / f"eda_{subset}_overview.png"
        plt.savefig(fig_path, dpi=300, bbox_inches="tight")
        print(f"Chart saved to: {fig_path}")
    plt.show()
    plt.close(fig)

    return df


# Dataset cleaning function
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+|https\S+", "", text, flags=re.MULTILINE)
    # Remove user mentions
    text = re.sub(r"@\w+", "", text)
    # hashtag removal, keep word content
    text = re.sub(r"#(\w+)", r"\1", text)
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_cleaned_dataset(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    df_clean = df.copy()
    df_clean["cleaned_text"] = df_clean[text_col].apply(clean_text)

    df_clean["is_modified"] = df_clean[text_col] != df_clean["cleaned_text"]
    _modified_count = df_clean["is_modified"].sum()
    _modified_ratio = _modified_count / len(df_clean)
    _modified_examples = df_clean[df_clean["is_modified"]][[text_col, "cleaned_text"]].head(5)

    print(f"\n========== Dataset Cleaning ==========")
    print(f"Total records: {len(df_clean)}")
    print(f"Modified records: {_modified_count} ({_modified_ratio:.2%})")

    print("\nExamples of modified entries:")
    print(_modified_examples)

    return df_clean

# run sentiment prediction using the model pipeline
def prediction_sentiment(pipe, data_list):
    outputs = pipe(data_list)
    print(f"\n========== Sentiment Prediction ==========")
    print(f"Total records: {len(outputs)}")
    print("\nSample predictions:")
    for i, res in enumerate(outputs[:5]):
        print(f"Text: {data_list[i]}")
        print(f"Predicted label: {res['label']}, Score: {res['score']:.4f}\n")
    
    pred_ids = [pc.SENTIMENT_LABELS_R[res["label"]] for res in outputs]
    return pred_ids


# Run test if this script is executed directly
if __name__ == "__main__":
    # check if the user is logged in to Hugging Face Hub
    if not check_huggingface_login():
        print("Please log in to Hugging Face Hub to proceed.")
        exit(1)
    
    # Load TweetEval dataset sentiment subset and check
    dataset = load_dataset(tec.REPO_ID, tec.SUBSET_SENTIMENT)

    # Check the structure of the test split
    # df_train = check_dataset_structure(dataset, subset=tec.SPLIT_TRAIN)
    # df_validation = check_dataset_structure(dataset, subset=tec.SPLIT_VALIDATION)

    # test split
    df_test = check_dataset_structure(dataset, subset=tec.SPLIT_TEST)
    df_test_eda = get_data_eda(df_test, subset=tec.SUBSET_SENTIMENT, save_image=True)
    df_clean = get_cleaned_dataset(df_test_eda, text_col="text")
    # model pipeline test
    # pipe_baseline = pipeline(
    #     task="text-classification",
    #     model=pc.BASELINE_MODEL_NAME,
    #     tokenizer=pc.BASELINE_MODEL_NAME,
    #     truncation=True,
    #     max_length=pc.MAX_LENGTH,
    #     batch_size=pc.BATCH_SIZE
    # )
    # pipe_prod = pipeline(
    #     task="text-classification",
    #     model=pc.PROD_MODEL_NAME,
    #     tokenizer=pc.PROD_MODEL_NAME,
    #     truncation=True,
    #     max_length=pc.MAX_LENGTH,
    #     batch_size=pc.BATCH_SIZE
    # )
    # # example prediction
    # p_baseline = prediction_sentiment(pipe_baseline, df_clean["cleaned_text"].tolist())
    # p_prod = prediction_sentiment(pipe_prod, df_clean["cleaned_text"].tolist())
    
