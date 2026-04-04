from langchain_openai import ChatOpenAI

class ChatModels:

    @staticmethod
    def LoadOpenaiChatModel(model_name='gpt-4.1-2025-04-14'):
        llm = ChatOpenAI(
            model=model_name
        )
        return llm