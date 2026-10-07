from data import *
from templates import *
from pathlib import Path

root_path = Path(__file__).parent.parent

templates = [templates_buying, template_scheduling, templates_deleting, templates_tracking, templates_returning, templates_inquiring, templates_editing]

entries = {
    "item": items,
    "replacement_item": items,
    "unit": units,
    "day": days,
    "event": events,
    "season": seasons,
    "certification": certifications,
    "time": range(1, 12),
    "returning_reason": returning_reasons,
    "returning_verb": returning_verbs,
    "returning_noun": returning_nouns,
    "deleting_reason": deleting_reasons,
    "deleting_verb": deleting_verbs,
    "deleting_noun": deleting_nouns,
    "number": range(1, 15),
    "order_id": range(1, 2341),
    "quantity": range(1, 15),
    "new_quantity": range(1, 15),
    "season": seasons,
    "condition": conditions
}

labels = ["buying", "scheduling", "deleting", "tracking", "returning", "inquiring", "editting", "finishing", "customer-service", "chitchat"]

def dataframe_manipulator(seed):
    data_generator = Generator(templates=templates, entries=entries, seed=seed)
    dataset = data_generator.generate(total_number=250)

    dataset.append(dataset_finishing)
    dataset.append(dataset_customer_service)
    chitchat_dataset = pd.read_csv(str(root_path / 'Datasets/chitchat_dataset.csv'))
    chitchat_dataset.drop("Unnamed: 0", axis=1, inplace=True)

    dataframe = pd.DataFrame()
    for i in range(len(dataset)):
        if labels[i] == "inquiring":
            dataset[i] = dataset[i] + faq_dataset
        dataframe = pd.concat((dataframe, to_pandas(dataset[i], labels[i])))
    dataframe = pd.concat((dataframe, chitchat_dataset))

    dataframe.reset_index(inplace=True, drop=True)
    indexes_to_drop = dataframe[dataframe["label"] == "inquiring"].sample(n=100, random_state=seed).index
    dataframe.drop(indexes_to_drop, axis=0, inplace=True)
    dataframe.reset_index(inplace=True, drop=True)

    dataframe.drop_duplicates(subset="text", inplace=True)
    dataframe = dataframe.sample(n=len(dataframe)).reset_index(drop=True)
    return dataframe

dataframe = dataframe_manipulator(385)
dataframe.to_csv(str(root_path / 'Datasets/original_intention_dataset.csv'), index=False)
