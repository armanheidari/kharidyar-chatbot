import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import os
from typing import List, Dict
from collections import Counter
from seaborn import barplot
from pathlib import Path

root_path = Path(__file__).parent.parent

class NER_DataGenerator:
    def __init__(self, templates: List[List[str]],  entries: Dict, labels: List[str], seed: int = 20) -> None:
        random.seed(seed)
        self.templates = templates
        self.entries = entries
        self.labels = labels
        self.count_entity = {key: 0 for key in self.entries.keys()}
        
    def generate(self, analyze: bool = False) -> None:
        dataset = []
        for i in range(len(self.labels)):
            dataset.append([None, None, None, self.labels[i]]) # In df fillna with previous value for intent col and then remove all rows with nan
            
            if i < len(self.templates):
                for _ in range(self.templates[i][1]):
                    data, add = self.__fill_templates(self.templates[i][0])
                    if add:
                        dataset.append(data)
        
        self.data = pd.DataFrame(dataset, columns=["text", "positions", "slots", "intent"])
        self.data["intent"] = self.data["intent"].fillna(method="ffill")
        self.data = self.data.dropna()
        
        if analyze:
            counter = Counter()
            self.data['slots'].apply(lambda d: counter.update(d.keys()))
            df_counter = pd.DataFrame.from_records(list(counter.items()), columns=['key', 'count'])
            plt.figure(figsize=(15,10), dpi=100)
            plt.xticks(rotation=45)
            barplot(x='key', y='count', data=df_counter)
            plt.title('Count of each key')
            plt.show()
        
    def save_data(self, name: str = "ner_data") -> None:  
        self.data.to_json(str(root_path / f"Datasets/{name}.json"), orient="records", force_ascii=False)
    
    def __generate_random_entries(self):
        templates_keys = self.entries.keys()
        templates_values = [random.choice(i[0]) for i in self.entries.values()]
        entries_dict = dict(zip(templates_keys, templates_values))
        entries_dict["date"] = f"{random.randint(1400, 1403)}/{random.randint(1, 12)}/{random.randint(1, 30)}"
        entries_dict["time"] = f"ساعت {random.randint(1, 12)}"
        entries_dict["number"] = f"روز {random.randint(1, 15)}"
        return entries_dict
    
    def __fill_templates(self, template):
        entries_dict = self.__generate_random_entries()
        chosen_sentence = random.choice(template)
        
        positions = {}
        slots = {}
        
        fixed_entries = {}
        excluded_entries = set(["deleting_reason", "returning_noun", "returning_reason", "returning_verb", "condition", "certification", "season"])
        for key, value in entries_dict.items():
            if key not in excluded_entries:
                fixed_entries["{" + key + "}"] = value
        
        placeholders = set(fixed_entries.keys())
        current_len = 0
        add = True
        for word in chosen_sentence.split():
            if word in placeholders:
                word = word[1:-1] # remove {}
                
                if self.count_entity[word] >= self.entries[word][1]:
                    add = False
                    break
                self.count_entity[word] += 1
                
                slots[word] = str(entries_dict[word])
                positions[word] = [
                    current_len,
                    current_len + len(str(entries_dict[word])) - 1]
            current_len += len(word) + 1 # 1 = space
            
        return (chosen_sentence.format(**entries_dict), positions, slots, None), add
    
