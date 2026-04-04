
from dotenv import load_dotenv
from src.config.config_chat_model import ChatModels


load_dotenv()
chat_model = ChatModels()

llm = chat_model.LoadOpenaiChatModel()

response = llm.invoke('hi')

print(response)



