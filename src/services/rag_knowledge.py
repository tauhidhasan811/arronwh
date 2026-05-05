from src.services.data_processor import DataProcessor
from src.hyper_parameters import params

class RagKnowledge:
    def __init__(self):
        self.path = params['knowledge_path']

    def update_knowledge(self):
        chunk = DataProcessor.create_chunk(self.path)
        ebd = DataProcessor.embedde_sentence(chunk)
        print(ebd.shape)
        
# print(chunk)

