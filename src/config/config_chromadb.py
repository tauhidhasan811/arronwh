import os
import chromadb
from src.hyper_parameters import params

class ChromaDB:
    def __init__(self):
        self.path = params['chromadb_path']
        os.makedirs(self.path, exist_ok=True)
        # os.environ["CHROMADB_DIRECTORY"] = self.path
        self.client = chromadb.PersistentClient(path=self.path)


    def store_knowledge(self, chunk: list, embedding: list, 
                         client_name: str = params['client_name']):

        collection = self.client.get_or_create_collection(client_name)
        metadata = [{'text': text} for text in chunk]

        collection.add(
            embeddings=embedding,
            metadatas=metadata,
            ids = [str(i) for i in range(len(chunk))]        
        )

        print("Successfully store data")
        return "Successfully store data"
    
    
    def find_relevent_text(self, embedding, num_neighbour = 3, 
                           client_name: str = params['client_name']):
        
        collection = self.client.create_collection(client_name)
        result = collection.query(query_embeddings=[embedding], n_results=num_neighbour)
        return result
    

