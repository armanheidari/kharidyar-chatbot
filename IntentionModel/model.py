from sklearn.svm import LinearSVC, SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import classification_report

class ModelDevelopment:
    def __init__(self):
        pass
        
    def compile(self, config, preprocessor, model, dataset):
        self.config = config
        self.preprocessor = preprocessor
        self.model = model
        self.x_set, self.y_set = dataset[self.config["features"]], dataset[self.config["label"]]
        self.__preprocess()
        
    def fit(self):
        self.model.fit(self.x_train, self.y_train)
        y_pred = self.model.predict(self.x_test)
        report = classification_report(self.y_test, y_pred)
        return self.model, report
    
    def parameter_tuning(self, type, config):
        if type == "grid_search":
            self.grid_search = GridSearchCV(
                estimator=self.model,
                param_grid=config["param_grid"],
                cv=config["cv"],
                n_jobs=-1,
            )
            self.grid_search.fit(self.x_set, self.y_set)
            return self.grid_search
        elif type == "randomized":
            self.randomized_search = RandomizedSearchCV(
                estimator=self.model,
                param_distributions=config["param_distributions"],
                n_iter=config["n_iter"],
                cv=config["cv"],
                n_jobs=-1,
                # error_score=0
            )
            self.randomized_search.fit(self.x_set, self.y_set)
            return self.randomized_search
            

    def __preprocess(self):
        self.x_set = self.x_set.apply(lambda x: self.preprocessor.fit(x))
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x_set, self.y_set, test_size=self.config["test_size"], stratify=self.y_set, random_state=self.config["seed"]
        )
    
    
class SVM:
    def __init__(self, config):
        self.config = config
        
    def compile(self):
        count_vectorizer = CountVectorizer(
            lowercase=False,
            ngram_range=self.config["ngram_range"],
            max_df=self.config["max_df"],
            min_df=self.config["min_df"]
        )
        tfidf_transformer = TfidfTransformer(
            sublinear_tf=self.config["sublinear_tf"]
        )
        svm = LinearSVC(
            loss=self.config["loss"],
            multi_class=self.config["multi_class"],
            C=self.config["C"]
        )
        model = Pipeline(
            [
                ("vectorizer", count_vectorizer),
                ("transformer", tfidf_transformer),
                ("classifier", svm)
            ]
        )
        return model
        