import re
from docx import Document
from typing import List, Dict
from api.schemas.chat_body import ChatHistoryItem

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