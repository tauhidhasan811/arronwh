from pydantic import BaseModel
from typing import Dict, List

class ChatHistoryItem(BaseModel):
    user_query: str
    ai_response: str


class Chatbody(BaseModel):
    previous_chat: List[ChatHistoryItem]
    user_query: str