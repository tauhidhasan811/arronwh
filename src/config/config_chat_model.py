from langchain_openai import ChatOpenAI
from src.hyper_parameters import params
from typing import Any

class ChatModels:

    @staticmethod
    def LoadOpenaiChatModel(model_name='gpt-4.1-2025-04-14', 
                            **kwargs)->ChatOpenAI:

        accepted_params = params['accepted_parameters']
        invalid_keys = [key for key in kwargs if key not in accepted_params]
        if invalid_keys:
            raise ValueError(f"Unsupported parameters: {invalid_keys}")

        config : dict[str: Any] = {
            'model': model_name
        }

        config.update(kwargs)
        llm = ChatOpenAI( **config)
        return llm         