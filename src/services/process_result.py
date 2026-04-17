from api.schemas.chat_body import Chatbody
from src.config.config_chat_model import ChatModels

class ProcessResult():
    def __int__(self):
        self.chatmodel = ChatModels()

    def chat_response(body: Chatbody):
        user_query = body.user_query
        previous_query = body.previous_chat
        


