from src.services.data_processor import DataProcessor
from src.config.config_chromadb import ChromaDB

path = r'data\files\YoloHeat Company Guide.docx'

chunk = DataProcessor.create_chunk(path)

data = ["hi !! how are you??"]

ebd = DataProcessor.embedde_sentence(data)
print(ebd.shape)
# print(chunk)

chroma_db = ChromaDB()

chroma_db.store_knowledge(chunk=data, embedding=ebd)