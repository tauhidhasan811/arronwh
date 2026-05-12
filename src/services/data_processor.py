import html
import re
import fitz
from docx import Document
from typing import List, Dict
from api.schemas.chat_body import ChatHistoryItem
# from src.config.config_embedding_model import Embedder
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DataProcessor:


    @staticmethod
    def clean_text(text):
        # Step 1: Remove all literal backslashes
        cleaned = text.replace("\\", "")

        # Step 2: Remove backticks (` or ``` )
        cleaned = re.sub(r"`{1,3}", "", cleaned)

        # Step 3: Remove HTML tags and decode HTML entities
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        cleaned = html.unescape(cleaned)

        # Step 4: Remove newlines and extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    
    @staticmethod
    def process_previous_history(previous_data:List[Dict]):
        max_chat = 10
        max_chars = 2000
        char_count = 0
        selected_chat = []
        idx = 0
        for data in reversed(previous_data):
            prev = str(data)
            prev = DataProcessor.clean_text(prev)
            current_chars = len(prev)
            if idx >= max_chat or char_count + current_chars > max_chars:
                break

            print(f"Current chat count : {idx + 1} && char count: {char_count}")
            char_count += current_chars
            if hasattr(data, "model_dump"):
                selected_chat.append(data.model_dump())
            else:
                selected_chat.append(data)
            idx += 1
        
        print('-' * 60)
        print(' ' * 10, 'Chat History process successfully.')
        print('-' * 60)
        print(f"Total Number of chars : {char_count}")
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
    def read_pdf(pdf_path: str):
        doc = fitz.open(pdf_path)

        extracted_text = ""
        for page_index, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                extracted_text += f"\n--- Page {page_index + 1} ---\n{text}"

        return extracted_text
    


    @staticmethod
    def file_reader_route(path:str):
        if path.endswith('.pdf'):
            data = {
                "is_read": True, 
                "data": DataProcessor.read_pdf(path)
            }
            
        elif path.endswith('.pdf'):
            data = {
                "is_read": True, 
                "data": DataProcessor.read_docx(path)
            }
        
        
        else:
            data = {
                "is_read": False, 
                "data": f"I can not read {path.split('.')[-1]}"
            }
            
        
        return data






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
    def embedde_sentence(sentences: List, ebd_model: SentenceTransformer):

        print(type(sentences))
        if type(sentences) is not list:
            print("Data type is not list")
            sentences = [sentences]
        embedding= []
        # ebd_model = Embedder().hugg_sentence_embedder()
        if __name__ == '__main__':
            pool = ebd_model.start_multi_process_pool()
            # embedding = ebd_model.encode(sentences)
            embedding = ebd_model.encode_multi_process(sentences, pool)
            ebd_model.stop_multi_process_pool(pool)
        if not embedding:
            embedding = ebd_model.encode(sentences)
        return embedding
