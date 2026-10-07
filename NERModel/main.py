from model import *
from ner_preprocessing import *
from transformers import AutoTokenizer
from tqdm import tqdm
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

root_path = Path(__file__).parent.parent

model_name = "HooshvareLab/bert-base-parsbert-uncased"

def create_model(model_name, dataset, name_of_file=None, train=True):
    all_texts = [i.text for i in dataset]
    all_slots = [i.slots for i in dataset]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    encoded_texts = encode_text(all_texts, tokenizer)

    max_len = encoded_texts[0][0].shape[0]
    slot_handler = SlotHandler(all_slots=all_slots)
    encoded_slots = slot_handler.encode_slots(all_texts, tokenizer, max_len=max_len)

    ner_config = {
        "model_name": model_name,
        "dropout_prob": 0.2,
        "slot_labels": len(slot_handler.le.classes_),
        "activation": "sigmoid"
    }

    train_config = {
        "learning_rate": 1e-4,
        "x": {"input_ids": encoded_texts[0], "token_type_ids": encoded_texts[2],  "attention_mask": encoded_texts[1]},
        "y": encoded_slots,
        "epochs": 2
    }

    ner_model = NERDetector(
        config=ner_config
    )
    
    if train == False:
        return ner_model, tokenizer, slot_handler.le.classes_
    
    else:
        history, model = ner_train(model=ner_model, config=train_config)
        model.save_weights(str(root_path / f'Models/{name_of_file}/ner_checkpoint'))
        return 0
    
  
dataset_0 = read_json_file(str(root_path / "Datasets/ner_dataset_0.json"))
dataset_1 = read_json_file(str(root_path / "Datasets/ner_dataset_1.json"))
dataset_2 = read_json_file(str(root_path / "Datasets/ner_dataset_2.json"))
datasets = [dataset_0, dataset_1]


if __name__ == "__main__":    
    for i in tqdm(range(len(datasets))):
        create_model(model_name=model_name, dataset=datasets[i], name_of_file=f"ner_model_{i}")
