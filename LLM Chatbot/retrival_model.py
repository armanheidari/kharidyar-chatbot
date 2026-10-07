from langchain.document_loaders import TextLoader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.neighbors import NearestNeighbors


class RetrievalModel:
    def __init__(self, file_path):
        loader = TextLoader(file_path, encoding='utf-8')
        self.documents = loader.load()

    def compile(self, config):
        self.config = config
        self.embedding_model = SentenceTransformer(config["model_name"])
        self.knn = NearestNeighbors(n_neighbors=config["n_neighbors"], metric=config["metric"])
        token_splitter = SentenceTransformersTokenTextSplitter(
            model_name=config["model_name"],
            chunk_overlap=config["chunk_overlap"], 
            tokens_per_chunk=config["tokens_per_chunk"]
        )
        docs = token_splitter.split_documents(self.documents)
        self.corpus = np.array([docs[i].page_content for i in range(len(docs))])
        
    def fit(self):
        embeddings = self.embedding_model.encode(self.corpus)
        self.knn.fit(embeddings)
    
    def invoke(self, query):
        query_embedding = self.embedding_model.encode(query)
        distances, indices = self.knn.kneighbors(query_embedding.reshape(1, -1))
        result = [self.corpus[indices[0][i]] if distances[0][i] < 0.8 else "" for i in range(len(indices[0]))]
        temp = []
        for i in result:
            if i != "":
                temp.append(i)
        result = temp
        return result
        