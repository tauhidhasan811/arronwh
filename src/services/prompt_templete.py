from langchain_core.prompts import PromptTemplate

def Prompt(user_input):
    instraction = f"You are a assiestent of the boiler company where sell boilders/product, controllers of that and extrals. Your task is answer of them and also call the tools if needed. ANswer the user query {user_input}"
    return instraction