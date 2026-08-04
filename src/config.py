from pathlib import Path

class ProjectConfig:
    # Project root directory
    ROOT_DIR = Path(__file__).parent.parent
    # Image output directory
    IMAGE_DIR = Path(ROOT_DIR) / "asset" / "images"
    # Create the image directory if it doesn't exist
    # IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    # Model config directory
    BASELINE_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    PROD_MODEL_NAME = "LYTinn/gpt2-finetuning-sentiment-model-3000-samples"
    MAX_LENGTH = 128
    BATCH_SIZE = 16


class TweetEvalConfig:
    # Dataset repository ID on Hugging Face Hub
    REPO_ID = "cardiffnlp/tweet_eval"

    # All available subsets in the TweetEval dataset
    SUBSET_EMOJI = "emoji"
    SUBSET_SENTIMENT = "sentiment"
    SUBSET_OFFENSIVE = "offensive"
    SUBSET_HATE = "hate"
    SUBSET_IRONY = "irony"
    SUBSET_EMOTION = "emotion"
    SUBSET_STANCE_ABORTION = "stance_abortion"
    SUBSET_STANCE_ATHEISM = "stance_atheism"
    SUBSET_STANCE_CLIMATE = "stance_climate"
    SUBSET_STANCE_FEMINIST = "stance_feminist"
    SUBSET_STANCE_HILLARY = "stance_hillary"

    # Data split options
    SPLIT_TRAIN = "train"
    SPLIT_VALIDATION = "validation"
    SPLIT_TEST = "test"

    # Sentiment labels mapping
    SENTIMENT_LABELS = {
            0: "negative",
            1: "neutral",
            2: "positive"
        }
    SENTIMENT_LABELS_R = {

        }





