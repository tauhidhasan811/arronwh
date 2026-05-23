from langchain_openai import ChatOpenAI
from src.hyper_parameters import params
from src.tools.database_tools import GetAllData
from src.tools.user_contact_info import SaveUserContactInfo
from typing import Any

class ChatModels:

    def __init__(self):
        self.model_name=params['model_name']

    def __config_llm(self, **kwargs)->ChatOpenAI:

        accepted_params = params['accepted_parameters']
        invalid_keys = [key for key in kwargs if key not in accepted_params]
        if invalid_keys:
            raise ValueError(f"Unsupported parameters: {invalid_keys}")

        config : dict[str: Any] = {
            'model': self.model_name
        }

        config.update(kwargs)
        llm = ChatOpenAI( **config)
        return llm
    

    def GetChatModel(self, **kwargs):
        llm = self.__config_llm(**kwargs)
        llm_with_tools = llm.bind_tools([GetAllData, SaveUserContactInfo])
        return llm_with_tools