import pandas as pd
from pathlib import Path
from pickle import dump
import sys
from scipy.stats import uniform

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / 'IntentionModel'))

from IntentionModel.model import *
from IntentionModel.preprocessor import *

dataset = pd.read_csv(str(root_path / 'Datasets/sentiment_dataset.csv'))

preprocessor = Preproccessing(
    spell_checking=False,
    lemmatizing=False,
    stemming=False 
)

config_model = {
    "ngram_range": (1, 1),
    "min_df": 1,
    "max_df": 0.8,
    "sublinear_tf": True,
    "loss": "squared_hinge",
    "multi_class": "ovr",
    "C": 5.8
}

param_grid = {
    # "ngram_range": (1, 2),
    "vectorizer__max_df": [0.005, 0.05, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9],
    "classifier__loss": ["squared_hinge", "hinge"],
    "classifier__C": [0.1, 0.5, 1, 5, 7, 10]
}

distribution = {
    "vectorizer__ngram_range": [(1, 1), {1, 2}, (1, 3), (2, 2)],
    "classifier__loss": ["squared_hinge", "hinge"],
    "vectorizer__max_df": uniform(),
    "classifier__C": uniform(loc=0, scale=15)
}

config_tune = {
    "param_distributions": distribution,
    "cv": 5,
    "n_iter": 200
}

svm_model = SVM(config=config_model)
svm_model = svm_model.compile()

config_dev = {
    "features": "text",
    "label": "label",
    "test_size": 0.2,
    "seed": 12
}

model_developmet = ModelDevelopment()
model_developmet.compile(
    config=config_dev,
    preprocessor=preprocessor,
    model=svm_model,
    dataset=dataset
)

## Perform the hyperparameter optimization ##
best_model = model_developmet.parameter_tuning(config=config_tune, type="randomized")
print(f"Best score: {best_model.best_score_}\n with parameter: {best_model.best_params_}")

## Saving the results ##
result = pd.DataFrame(best_model.cv_results_).sort_values(by="mean_test_score", axis=0, ascending=False)
result[["param_classifier__C", "param_classifier__loss", "param_vectorizer__max_df", "param_vectorizer__ngram_range", "mean_test_score", "std_test_score"]].to_excel(str(root_path / 'Results/hyperparameter_tuning_sentiment_model.xlsx'))

# result, report = model_developmet.fit()
# print(report)

## Saving the model ##
save = input("\nDo you want to save the model? [Y/N] ")
if save.lower() == "y":
    with open(str(root_path / 'Models/sentiment_recognizer_model_2.pkl'), "wb") as f:
        dump(best_model, f, protocol=5)