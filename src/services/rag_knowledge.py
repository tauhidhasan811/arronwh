from src.services.data_processor import DataProcessor
from src.config.config_chromadb import ChromaDB
from sentence_transformers import SentenceTransformer
from src.hyper_parameters import params

class RagKnowledge:
    def __init__(self, embedding_model: SentenceTransformer):
        self.path = params['knowledge_path']
        self.chroma_db = ChromaDB()
        self.embedding_model = embedding_model

    def update_knowledge(self):
        chunk = DataProcessor.create_chunk(self.path)
        ebd = DataProcessor.embedde_sentence(chunk, ebd_model=self.embedding_model)
        print(ebd.shape)
        message = self.chroma_db.store_knowledge(chunk=chunk, embedding=ebd)
        return message
    
    def retrive_chunk(self, text):

        ebd = DataProcessor.embedde_sentence(text,  ebd_model=self.embedding_model)
        chunks = self.chroma_db.find_relevent_text(ebd)
        return chunks
        
# print(chunk)

