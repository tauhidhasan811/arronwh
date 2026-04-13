
import json
from fastapi import FastAPI
from src.config.config_chat_model import ChatModels
from src.services.prompt_templete import Prompt

llm = ChatModels().GetChatModel()

data = ''
while data != "exit":
    data = input("Enter text : ")
    prompt = Prompt(user_input=data)
    response = llm.invoke(prompt)
    print(response)
