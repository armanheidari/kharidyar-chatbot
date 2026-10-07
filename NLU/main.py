from nlu import NLU
import sys
from pickle import load
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(1, str(root_path))

from NERModel.main import *
from NERModel.model import *

model_name = "HooshvareLab/bert-base-parsbert-uncased"

## Creating the NER models
model_1, tokenizer, slot_names_1 = create_model(model_name=model_name, dataset=dataset_0, train=False)
model_2, tokenizer, slot_names_2 = create_model(model_name=model_name, dataset=dataset_1, train=False)
model_3, tokenizer, slot_names_3 = create_model(model_name=model_name, dataset=dataset_2, train=False)

# ## Loading the NER model weights
model_1.load_weights(str(root_path / "Models/ner_model_0/ner_checkpoint"))
model_2.load_weights(str(root_path / "Models/ner_model_1/ner_checkpoint"))
model_3.load_weights(str(root_path / "Models/ner_model_2/ner_checkpoint"))

## Loading Intention Recognizer models
with open(str(root_path / "Models/intention_recognizer_model_2.pkl"), "rb") as f:
    intent_classifier = load(f)
    
with open(str(root_path / "Models/intention_recognizer_model_without_faq.pkl"), "rb") as f:
    intent_classifier_2 = load(f)
    
## Loading Sentiment Recognizer models
with open(str(root_path / "Models/sentiment_recognizer_model_2.pkl"), "rb") as f:
    sentiment_classifier = load(f)
    

# Configuration
config_nlu = {
    "tokenizer": tokenizer,
    "ner_model_1": model_1,
    "ner_model_2": model_2,
    "ner_model_3": model_3,
    "ner_slots_1": slot_names_1,
    "ner_slots_2": slot_names_2,
    "ner_slots_3": slot_names_3,
    "intent_model": intent_classifier,
    "intent_model_2": intent_classifier_2,
    "sentiment_model":sentiment_classifier
}

if __name__ == "__main__":
    nlu = NLU(config=config_nlu)
    print(nlu.inference("شیر هاتون از کجا تولید شده است؟"))