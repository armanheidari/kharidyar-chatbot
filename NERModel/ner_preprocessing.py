from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import numpy as np
from hazm import *

# pos_tagger = POSTagger(model = 'pos_tagger.model')
hazm_tokenizer = WordTokenizer()

E2P_map = {'1' : '۱', '2' : '۲', '3' : '۳', '4' : '۴', '5' : '۵', '6' : '۶', '7' : '۷', '8' : '۸', '9' : '۹', '0' : '۰' }
def convert_number_to_persian(strIn : str):
    a = map(lambda ch: E2P_map[ch] if ch in E2P_map else ch, strIn)
    return ''.join(list(a))

import json
import os

class RawData(object):
    def __init__(self, id, intent, positions, slots, text):
        self.id = id
        self.intent = intent
        self.positions = positions
        self.slots = slots
        self.text = text

    def __repr__(self):
        return str(json.dumps(self.__dict__, indent=2, ensure_ascii=False))


def read_json_file(filename):
    if os.path.exists(filename):
        intents = []

        with open(filename, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

            for k in data:
                intent = k["intent"]
                positions = k["positions"]
                slots = k["slots"]
                text = k["text"]

                temp = RawData(k, intent, positions, slots, text)
                intents.append(temp)

        return intents
    else:
        raise FileNotFoundError("No file found with that path!")


def encode_text(texts, tokenizer):
    tokenized_texts = tokenizer(
        text=texts,
        padding=True,
        truncation=True,
        return_tensors="tf"
    )
    input_ids = tokenized_texts["input_ids"]
    attention_mask = tokenized_texts["attention_mask"]
    token_type_ids = tokenized_texts["token_type_ids"]
    return input_ids, attention_mask, token_type_ids

def encode_intents(intents):
    le = LabelEncoder()
    encoded_intents = le.fit_transform(intents)
    encoded_intents = tf.convert_to_tensor(encoded_intents, dtype="int32")
    return encoded_intents, le

def encode_pos(all_texts, tokenizer, max_len):
    label_dict = {} 
    encoded_pos = np.zeros(shape=(len(all_texts), max_len), dtype=np.int32)
    index = 0
    for idx, text in enumerate(all_texts):
        enc = []
        text = convert_number_to_persian(text)
        tokens = hazm_tokenizer.tokenize(text)
        tags = pos_tagger.tag(tokens)
        for i in range(len(tokens)):
            bert_tokens = tokenizer.tokenize(tokens[i])
            if tags[i][1] in label_dict.keys():
                label = label_dict[tags[i][1]]
            else:
                label_dict[tags[i][1]] = index
                label = index
                index += 1
            enc.extend([label] * (len(bert_tokens)))
        encoded_pos[idx, 1:len(enc) + 1] = enc
    return encoded_pos
    

class SlotHandler:
    def __init__(self, all_slots):
        self.slots = all_slots
        self.le = LabelEncoder()
        self.hazm_tokenizer = WordTokenizer()
        self.__label_encoder()
        
    def encode_slots(self, all_texts, tokenizer, max_len):
        encoded_pos = np.zeros(shape=(len(all_texts), max_len), dtype=np.int32)
        for idx, text in enumerate(all_texts):
            enc = []
            slot_names = self.slots[idx]
            tokens = self.hazm_tokenizer.tokenize(text)
            for token in tokens:
                bert_tokens = tokenizer.tokenize(token)
                token_slot_name = self.__word_to_slot(token, slot_names)
                if token_slot_name is not None:
                    enc.extend([self.le.transform([token_slot_name])[0]] * (len(bert_tokens)))
                else:
                    enc.append(0)
            encoded_pos[idx, 1:len(enc) + 1] = enc
        return encoded_pos    
    
    def __label_encoder(self):
        slot_names = []
        for i in self.slots:
            for j in list(i.keys()):
                slot_names.append(j)
        slot_names = list(set(slot_names))
        slot_names.insert(0, "<PAD>")
        self.le.fit(slot_names)
        return self.le
    
    def __word_to_slot(self, word, slot_dict):
        for slot_label, value in slot_dict.items():
            if word in value.split():
                return slot_label
        return None


if __name__ == "__main__":
    texts = ["4 کیلو مرغ میخوام"]
    print([convert_number_to_persian(text) for text in texts])