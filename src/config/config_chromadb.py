import os
import chromadb
from src.hyper_parameters import params
from src.services.delete_path import force_delete_folder

class ChromaDB:
    def __init__(self):
        self.path = params['chromadb_path']
        if os.path.exists(self.path):
            force_delete_folder(path = self.path)
        os.makedirs(self.path, exist_ok=True)
        # os.environ["CHROMADB_DIRECTORY"] = self.path
        self.client = chromadb.PersistentClient(path=self.path)


    def store_knowledge(self, chunk: list, embedding: list, 
                         client_name: str = params['client_name']):
        
        if client_name in self.client.list_collections():
            self.client.delete_collection(client_name)
        collection = self.client.get_or_create_collection(client_name)
        # metadata = [{'text': text} for text in chunk]
        metadata = chunk

        collection.add(
            embeddings=embedding,
            documents=metadata,
            ids = [str(i) for i in range(len(chunk))]        
        )

        print("Successfully store data")
        return "Successfully store data"
    
    
    def find_relevent_text(self, embedding, num_neighbour = 3, 
                           client_name: str = params['client_name']):
        
        collection = self.client.get_or_create_collection(client_name)
        result = collection.query(query_embeddings=embedding.tolist(), n_results=num_neighbour)
        text = ''
        for doc in result['documents']:
            text+= "\n" +str(doc)
        return text
    

