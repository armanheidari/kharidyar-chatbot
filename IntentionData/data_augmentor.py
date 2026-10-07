from data import *
from pathlib import Path
from templates import *
import pandas as pd

root_path = Path(__file__).parent.parent

augmented_df = pd.read_csv(str(root_path / 'Datasets/augmented_intention_dataset(1).csv'))
original_df = pd.read_csv(str(root_path / 'Datasets/original_intention_dataset.csv'))

mask_augment_config = {
    "corpus": dataset_finishing,
    "model_name": "HooshvareLab/bert-base-parsbert-uncased",
    "type": "mask_filling"
    
}

mask_augment_config_2 = {
    "corpus": dataset_customer_service,
    "model_name": "HooshvareLab/bert-base-parsbert-uncased",
    "type": "mask_filling"
    
}

finishing_augmented = augment(config=mask_augment_config)
finishing_df = pd.DataFrame({"text": finishing_augmented, "label": "finishing"})

customer_augmented = augment(config=mask_augment_config_2)
customer_df = pd.DataFrame({"text": customer_augmented, "label": "customer-service"})

## Mege Alltogether ##
intention_dataset = pd.concat([original_df, augmented_df, finishing_df, customer_df], axis=0)
intention_dataset.drop_duplicates(subset="text", inplace=True)
intention_dataset = intention_dataset.sample(n=len(intention_dataset)).reset_index(drop=True)
intention_dataset.to_csv(str(root_path / 'Datasets/intention_dataset.csv'), index=False)
