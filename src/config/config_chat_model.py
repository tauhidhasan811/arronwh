from langchain_openai import ChatOpenAI

class ChatModels:

    @staticmethod
    def LoadOpenaiChatModel(model_name='gpt-4.1-2025-04-14', *kwargs):
        
        llm = ChatOpenAI(
            model=model_name,
            temperature= 1,
            streaming=True
        )
        return llm