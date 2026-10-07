from pathlib import Path
import sys

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / 'IntentionData'))

from IntentionData.data import *
import pandas as pd

root_path = Path(__file__).parent.parent

## Data Wrangling ##
augmented_df = pd.read_csv(str(root_path / 'Datasets/augmented_sentiment_dataset.csv'))
original_df = pd.read_csv(str(root_path / 'Datasets/original_sentiment_dataset.csv'))
original_df.drop("Unnamed: 0", axis=1, inplace=True)

negative_augmented = pd.read_csv(str(root_path / 'Datasets/augmented_negative_sentiment_dataset.csv'))
negative_augmented.drop("Unnamed: 0", axis=1, inplace=True)

neutral_df = pd.read_csv(str(root_path / 'Datasets/translation.csv'), header=None)
neutral_df.columns = ["text", "label"]
neutral_df = neutral_df[neutral_df["label"] == 0]
neutral_df = neutral_df.sample(len(neutral_df) - 1000).reset_index(drop=True)

neutral_df_2 = pd.read_csv(str(root_path / 'Datasets/intention_dataset.csv'))
neutral_df_2 = neutral_df_2.query("label == 'finishing' | label == 'buying' | label == 'tracking' | label == 'chitchat' | label == 'inquiring' | label == 'scheduling'")
neutral_df_2.loc[:, "label"] = 0


mask_augment_config = {
    "corpus": original_df[original_df["label"] == 1]["text"].to_numpy(),
    "model_name": "HooshvareLab/bert-base-parsbert-uncased",
    "type": "mask_filling"
    
}

# negative_augmented = augment(config=mask_augment_config)
# negative_df = pd.DataFrame({"text": negative_augmented, "label": "1"})
# negative_df.to_csv(str(root_path / 'Datasets/augmented_negative_sentiment_dataset.csv'))

## Mege Alltogether ##
intention_dataset = pd.concat([original_df, augmented_df, negative_augmented], axis=0)
intention_dataset.drop_duplicates(subset="text", inplace=True)

## Post Processing ##
intention_dataset.loc[intention_dataset["label"] == 1, "label"] = -1
intention_dataset.loc[intention_dataset["label"] == 0, "label"] = 1
intention_dataset = pd.concat([intention_dataset, neutral_df, neutral_df_2], axis=0)
intention_dataset = intention_dataset.sample(n=len(intention_dataset)).reset_index(drop=True)
intention_dataset.dropna(inplace=True)
intention_dataset.to_csv(str(root_path / 'Datasets/sentiment_dataset.csv'), index=False)