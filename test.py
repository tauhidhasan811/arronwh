# import time 

# from src.services.data_processor import DataProcessor
# from src.config.config_chromadb import ChromaDB
# from src.services.delete_path import force_delete_folder

# path = r'data\files\YoloHeat Company Guide.docx'

# chunk = DataProcessor.create_chunk(path)

# data = ["hi !! how are you??"]

# ebd = DataProcessor.embedde_sentence(data)
# print(ebd.shape)
# # print(chunk)

# force_delete_folder(path = 'data/chroma_db')
# time.sleep(30)
# chroma_db = ChromaDB()

# chroma_db.store_knowledge(chunk=data, embedding=ebd)

from src.services.rag_knowledge import RagKnowledge
from src.config.config_embedding_model import Embedder

embedder = Embedder().hugg_sentence_embedder()
rag = RagKnowledge(embedding_model=embedder)

# print(rag.update_knowledge())
text = "What service do you give??"

chunks = rag.retrive_chunk(text)

print(chunks)