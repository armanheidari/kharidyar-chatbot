from NER_Data_Generator import *
from NER_Data_Templates import *

labels = ["buying", "scheduling", "deleting", "tracking", "discount", "returning", "inquiring", "editting", "finishing", "chitchat"]

default_max_entity = 1500

entries = {
    "item": (items, default_max_entity),
    "replacement_item": (items, default_max_entity),
    "quantity": (list(range(1, 15)) + numbers, default_max_entity),
    "new_quantity": (list(range(1, 15)) + numbers, default_max_entity),
    "unit": (units, default_max_entity),
    "day": (days, default_max_entity),
    "event": (events, default_max_entity),
    "order_id": (list(range(1, 100)) + numbers, default_max_entity),
    "deleting_noun": (deleting_nouns, default_max_entity),
    
    "time": ([1, 2], default_max_entity),
    "date": ([1, 2], default_max_entity),
    "number": ([1, 2], default_max_entity),
    
    "season": (seasons, default_max_entity),
    "certification": (certifications, default_max_entity),
    "returning_reason": (returning_reasons, default_max_entity),
    "returning_noun": (returning_nouns, default_max_entity),
    "returning_verb": (returning_verbs, default_max_entity),
    "deleting_reason": (deleting_reasons, default_max_entity),
    "deleting_verb": (deleting_verbs, default_max_entity),
    "condition": (conditions, default_max_entity)
}

default_data_no = 50

templates_0 = [
    (templates_buying, 150),
    (templates_inquiring, 100),
] 
label_0 = ["buying", "inquiring"]

templates_1 = [
    (templates_editing, 200),
    (templates_deleting, 80),
] 
label_1 = ["editing", "deleting"]

templates_2 = [
    (templates_scheduling, 80),
    (templates_tracking, 50),
    (templates_returning, 40),
]
label_2 = ["scheduling", "tracking", "returning"]

templates_set = [templates_0, templates_1]
labels_set = [label_0, label_1]


for i in range(len(templates_set)):
    gen = NER_DataGenerator(templates_set[i], entries, labels_set[i])
    gen.generate(analyze=False)
    gen.save_data(name=f"ner_dataset_{i}")
