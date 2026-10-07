import numpy as np
import random
import pandas as pd
from googletrans import Translator
from tqdm import tqdm
from hazm import *
from transformers import pipeline
import string

def to_pandas(array, label):
    dataset = np.array([[i, f"{label}"] for i in array])
    df = pd.DataFrame(dataset)
    df.columns = ["text", "label"]
    return df

def augment(config):
    augmentor = Augmentor(config=config)
    translated_corpus = augmentor.augment()
    return translated_corpus

class Generator:
    def __init__(self, templates, entries, seed=20):
        random.seed(seed)
        self.templates = templates
        self.entries = entries
        
    def generate(self, total_number):
        dataset = []
        for template in self.templates:
            dataset.append([self.__fill_templates(template) for _ in range(total_number)])
        return dataset
        
    def __generate_random_entries(self):
        templates_keys = self.entries.keys()
        templates_values = [random.choice(i) for i in self.entries.values()]
        entries_dict = dict(zip(templates_keys, templates_values))
        entries_dict["date"] = f"{random.randint(1400, 1403)}/{random.randint(1, 12)}/{random.randint(1, 30)}"
        return entries_dict
    
    def __fill_templates(self, template):
        entries_dict = self.__generate_random_entries()
        chosen_sentence = random.choice(template)
        return chosen_sentence.format(**entries_dict)
        

class Augmentor:
    def __init__(self, config):
        self.corpus = config["corpus"]
        self.translator = Translator()
        self.classifier = pipeline(model=config["model_name"], task="fill-mask")
        self.type = config["type"]
    
    def augment(self):
        translated_corpus = []
        for sentence in tqdm(self.corpus):
            if self.type == "back_translation":
                translated = self.__back_translator(sentence)
                if isinstance(translated, int):
                    translated_corpus.append(translated)
                else:
                    translated_corpus.append(translated.text)
            else:
                translated = self.__mask_filling(sentence)
                translated_corpus = translated_corpus + translated
        return translated_corpus
    
    def __mask_filling(self, sentence):
        augmented = []
        tokenizer = WordTokenizer()
        i = 0
        while True:
            list_sentence = tokenizer.tokenize(sentence)
            rep = len(list_sentence) // 5 + 1
            random_chosen = random.choice(list_sentence)
            if random_chosen in string.punctuation + "،" + "؟":
                continue
            list_sentence[list_sentence.index(random_chosen)] = "[MASK]"
            masked_sentence = " ".join(list_sentence)
            augmented_sentence = self.classifier(masked_sentence)
            if augmented_sentence[0]["token_str"] != random_chosen and augmented_sentence[0]["sequence"] not in augmented:
                augmented.append(augmented_sentence[0]["sequence"])
                i += 1
            elif augmented_sentence[1]["token_str"] != random_chosen and augmented_sentence[1]["sequence"] not in augmented:
                augmented.append(augmented_sentence[1]["sequence"])
                i += 1
            else:
                continue
            if i > rep:
                break
        return augmented
    
    def __back_translator(self, sentence):
        try:
            translate_to_en = self.translator.translate(sentence, src='auto', dest='en')
            translate_to_fa = self.translator.translate(translate_to_en.text, src='auto', dest='fa')

            if translate_to_fa == sentence:
                translate_to_fr = self.translator.translate(sentence, src='auto', dest='fr')
                translate_to_fa = self.translator.translate(translate_to_fr.text, src='auto', dest='fa')

            if translate_to_fa == sentence:
                translate_to_de = self.translator.translate(sentence, src='auto', dest='de')
                translate_to_fa = self.translator.translate(translate_to_de.text, src='auto', dest='fa')

            if translate_to_fa == sentence:
                translate_to_es = self.translator.translate(sentence, src='auto', dest='es')
                translate_to_fa = self.translator.translate(translate_to_es.text, src='auto', dest='fa')

            if translate_to_fa == sentence:
                translate_to_ar = self.translator.translate(sentence, src='auto', dest='ar')
                translate_to_fa = self.translator.translate(translate_to_ar.text, src='auto', dest='fa')

            if translate_to_fa == sentence:
                return 0

            return translate_to_fa
        except:
            return -1