from ner_preprocessing import *
import silence_tensorflow.auto
import tensorflow as tf
from transformers import TFBertModel


class NERDetector(tf.keras.Model):
    def __init__(self, config):
        super().__init__(name="ner_detector")
        self.bert = TFBertModel.from_pretrained(config["model_name"])
        self.dropout = tf.keras.layers.Dropout(config["dropout_prob"])
        self.slot_classifier = tf.keras.layers.Dense(
            units=config["slot_labels"],
            activation=config["activation"],
            name="slot_classifier"
        )

    def call(self, inputs, **kwargs):
        trained_bert = self.bert(inputs, **kwargs)
        sequence_output = trained_bert.last_hidden_state
        sequence_output = self.dropout(
            sequence_output,
            training=kwargs.get("training", False)
        )
        slot_logits = self.slot_classifier(sequence_output)
        return slot_logits
    
def ner_train(model, config):
    opt = tf.keras.optimizers.Adam(config["learning_rate"], epsilon=1e-08)
    metrics = [tf.keras.metrics.SparseCategoricalAccuracy("accuracy")]
    model.compile(
        optimizer=opt, 
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=metrics
    )
    history = model.fit(
        x=config["x"], 
        y=config["y"], 
        epochs=config["epochs"], 
        batch_size=32, 
        shuffle=True
    )
    return history, model
    

def infer_ner(text, config):
    inputs = tf.constant(config["tokenizer"].encode(text))[None, :] 
    outputs = config["model"](inputs)
    slot_ids = outputs.numpy().argmax(axis=-1)[0, :]
    
    info = {"slots": {}}
    out_dict = {}
    predicted_slots = set([config["slot_names"][s] for s in slot_ids if s != 0])
    for ps in predicted_slots:
      out_dict[ps] = []

    tokens = config["tokenizer"].tokenize(text, add_special_tokens=True)
    for token, slot_id in zip(tokens, slot_ids):
        slot_name = config["slot_names"][slot_id]
        if slot_name == "<PAD>":
            continue
        collected_tokens = [token]
        idx = tokens.index(token)
        if token.startswith("##"):
          if tokens[idx - 1] not in out_dict[slot_name]:
            collected_tokens.insert(0, tokens[idx - 1])
        out_dict[slot_name].extend(collected_tokens)
        
    for slot_name in out_dict:
        tokens = out_dict[slot_name]
        slot_value = config["tokenizer"].convert_tokens_to_string(tokens)
        info["slots"][slot_name] = slot_value.strip()

    return info
