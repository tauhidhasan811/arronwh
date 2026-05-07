from langchain_openai.embeddings import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        self.model_name = model_name

    def hugg_sentence_embedder(self) -> SentenceTransformer:
        model = SentenceTransformer(self.model_name)
        return model
    