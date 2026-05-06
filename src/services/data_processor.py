import re
from docx import Document
from typing import List, Dict
from api.schemas.chat_body import ChatHistoryItem
from src.config.config_embedding_model import Embedder
from langchain_text_splitters import RecursiveCharacterTextSplitter
class DataProcessor:
    @staticmethod
    def CleanData(text):
        
        return
    
    @staticmethod
    def process_previous_history(previous_data:List[Dict]):
        min_chat = 2
        max_token = 100
        token_count = 0
        selected_chat = []
        idx = 1
        for data in reversed(previous_data):
            prev = str(data)
            current_token = len(prev)
            if token_count <= max_token or idx <= min_chat:
                print(f"Current chat count : {idx} && token count: {token_count}")
                token_count += current_token
                selected_chat.append(data.model_dump())
                idx+=1
            
            else:
                break
        
        print('-' * 60)
        print(' ' * 10, 'Chat History process successfully.')
        print('-' * 60)
        print(f"Total Number of token : {token_count}")
        print(f"Total Chat taken      : {idx}")

        return list(reversed(selected_chat))
    
    @staticmethod
    def read_docx(file_path):
        document = Document(file_path)
        text = []
        para_num = 0
        for paragraph in document.paragraphs:
            text.append(paragraph.text)
            para_num += 1
        print(f"Total number of paragraph : {para_num}")
        return '\n'.join(text)
    

    @staticmethod
    def create_chunk(file_path: str, chunk_size=300, chunk_overlap = 50):
        if not file_path.endswith(".docx"):
            return ValueError("Only accepted docx type")
        docs_data = DataProcessor.read_docx(file_path=file_path)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,      # Target number of characters per chunk
            chunk_overlap=chunk_overlap,    # Number of characters to repeat from the previous chunk
            length_function=len,
            separators=[ " ", "", "\n\n", "\n"] # Hierarchical separators
        )
        chunks = text_splitter.split_text(docs_data)

        return chunks


    @staticmethod
    def embedde_sentence(sentences: List):
        print(type(sentences))
        if type(sentences) is not list:
            print("Data type is not list")
            sentences = [sentences]
        
        ebd_model = Embedder().hugg_sentence_embedder()
        embedding = ebd_model.encode(sentences)
        return embedding
