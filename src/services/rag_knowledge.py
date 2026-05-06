from src.services.data_processor import DataProcessor
from src.config.config_chromadb import ChromaDB
from src.hyper_parameters import params

class RagKnowledge:
    def __init__(self):
        self.path = params['knowledge_path']
        self.chroma_db = ChromaDB()

    def update_knowledge(self):
        chunk = DataProcessor.create_chunk(self.path)
        ebd = DataProcessor.embedde_sentence(chunk)
        print(ebd.shape)
        message = self.chroma_db.store_knowledge(chunk=chunk, embedding=ebd)
        return message
    
    def retrive_chunk(self, text):

        ebd = DataProcessor.embedde_sentence(text)
        chunks = self.chroma_db.find_relevent_text(ebd)
        return chunks
        
# print(chunk)

