import os
import chromadb
from src.hyper_parameters import params

class ChromaDB:
    def __init__(self):
        self.path = params['chromadb_path']


    # def strore_knowledge(chunk: list, embedding: list):
