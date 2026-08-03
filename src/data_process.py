from datasets import load_dataset
import pandas as pd
from huggingface_hub import whoami, login

# check huggingface login status
# key : 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
def check_huggingface_login():
    try:
        user_info = whoami()
        print(f"Logged in as: {user_info['name']}")
    except Exception as e:
        login()  # Prompt user to log in
        print("Please log in to Hugging Face Hub to access datasets.")
    

# check the test structure
def check_dataset_structure(dataset, subset, max_records=10):
    if not isinstance(dataset, dict):
        print("Dataset is not a dictionary.")
        return None

    print(f"------------------------------------------------")
    print(f"Checking structure of the '{subset}' subset...")
    df = pd.DataFrame(dataset[subset])

    print("Dataset columns:", df.columns.tolist())
    print("Total records:", len(df))
    print("\nSample data preview:")
    print(df.head(max_records))
    print("\nLabel distribution:")
    print(df['label'].value_counts())
    return df

# Run test if this script is executed directly
if __name__ == "__main__":
    # check if the user is logged in to Hugging Face Hub
    check_huggingface_login()
    
    # Load TweetEval dataset (fixed full repo id)
    dataset = load_dataset("cardiffnlp/tweet_eval", "sentiment")
    df_test = check_dataset_structure(dataset, subset="test")