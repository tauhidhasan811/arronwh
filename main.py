"""
import json
from fastapi import FastAPI
from src.config.config_chat_model import ChatModels
from src.services.prompt_templete import Prompt
from src.tools.database_tools import GetAllData
llm = ChatModels().GetChatModel()

data = ''
while data != "exit":
    data = input("Human input : ")
    prompt = Prompt(user_input=data)
    response = llm.invoke(prompt)
    tools = response.tool_calls
    for tool in tools:
        name = tool['name']
        body = tool['args']['body']
        result = GetAllData.invoke(tool['args'])
        print(name)
        print(result)
    # print(response)
    print(f'AI response : {response.content}')
    print('\n\n')
"""


from fastapi import FastAPI
from api.router.chat_route import router as chat_router




app = FastAPI()

app.include_router(chat_router)
