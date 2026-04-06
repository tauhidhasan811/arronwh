
from dotenv import load_dotenv
from src.config.config_chat_model import ChatModels


load_dotenv()
chat_model = ChatModels()

llm = chat_model.LoadOpenaiChatModel(model_name='gpt-4.1-2025-04-14', temperature = 0.7)
response = llm.invoke('hi')

print(response.content)



