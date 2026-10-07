from pathlib import Path
import sys
import re

root_path = Path(__file__).parent.parent
sys.path.insert(1, str(root_path))

from IntentionModel.preprocessor import Preproccessing
from NERModel.main import infer_ner
    
    
class NLU:
    def __init__(self, config):
        self.config = config
        self.preprocessor = Preproccessing(stemming=False)
        self.category_1 = ["buying", "inquiring"]
        self.category_2 = ["editting"]
        self.category_3 = ["scheduling", "tracking", "returning", "deleting"]
        
        self.config_1 = {
            "model": self.config["ner_model_1"],
            "tokenizer": self.config["tokenizer"],
            "slot_names": self.config["ner_slots_1"]
        }
        
        self.config_2 = {
            "model": self.config["ner_model_2"],
            "tokenizer": self.config["tokenizer"],
            "slot_names": self.config["ner_slots_2"]
        }
        
        self.config_3 = {
            "model": self.config["ner_model_3"],
            "tokenizer": self.config["tokenizer"],
            "slot_names": self.config["ner_slots_3"]
        }
    
    def inference(self, input, predefined_intent=None):
        sentiment = self.get_sentiment(input)[0]
        secondary_intent = None
        if predefined_intent is not None:
            intent = predefined_intent
        else:
            intent = self.get_intention(input)[0]
        
        if intent in self.category_1:
            if intent == "inquiring":
                input = self.preprocessor.fit(input)
                secondary_intent = self.config["intent_model_2"].predict([input])[0]
            named_entities = self.get_named_entities(input, self.config_1)
        
        elif intent in self.category_2:
            named_entities = self.get_named_entities(input, self.config_2)
            
        elif intent in self.category_3:
            order_id = re.findall(r'\d+', input)
            if order_id != []:
                named_entities = {"slots": {"order_id": order_id[0]}}
            else:
                named_entities = {"slots": None}
        else:
            named_entities = {"slots": None}
        
        output = named_entities | {"sentiment": sentiment, "intent": intent, "secondary_intent": secondary_intent}
        return output
    
    def get_intention(self, input):
        input = self.preprocessor.fit(input)
        intent = self.config["intent_model"].predict([input])
        return intent
    
    def get_named_entities(self, input, config):
        named_entities = infer_ner(
            text=input,
            config=config
        )
        return named_entities
    
    def get_sentiment(self, input):
        input = self.preprocessor.fit(input)
        sentiment = self.config["sentiment_model"].predict([input])
        return sentiment
    