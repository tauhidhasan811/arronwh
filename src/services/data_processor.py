import re
from typing import List, Dict
from api.schemas.chat_body import ChatHistoryItem

class DataProcessor:
    @staticmethod
    def CleanData(text):
        
        return
    
    @staticmethod
    def process_previous_history(previous_data:List[Dict]):
        min_chat = 5
        max_token = 1000
        token_count = 0
        selected_chat = []
        idx = 0
        for data in reversed(previous_data):
            idx+=1
            prev = str(data)
            current_token = len(prev)
            if token_count <= max_token or idx <= min_chat:
                token_count += current_token
                selected_chat.append(data)
            
            else:
                break
        
        print('-' * 60)
        print(' ' * 20, 'Chat History process successfully.')
        print('-' * 60)
        print(f"Total Number of token : {token_count}")
        print(f"Total Chat taken      : {idx}")
        return selected_chat
    