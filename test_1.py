from langchain_openai import ChatOpenAI
from src.hyper_parameters import params
from src.tools.database_tools import GetAllData
from typing import Any


from dotenv import load_dotenv
load_dotenv()

config : dict[str: Any] = {
    'model': params['model_name']
    }

llm = ChatOpenAI( **config)

print(llm.invoke("hi"))

    