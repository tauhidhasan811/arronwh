from typing import List, Dict
from langchain_core.prompts import PromptTemplate
from langchain.messages import HumanMessage, SystemMessage, AIMessage


def Prompt(user_query, previous_chat: List[Dict]):
    sys_message = SystemMessage(
        content=f"You are a assiestent of the boiler company where sell boilders/product, controllers of that and extrals. Your task is answer of them and also call the tools if needed. Answer the user query"
    )

    hum_message = HumanMessage(
        content= f'Current user Query: {user_query} \n\n Previous Chat : {previous_chat}'
    )
    temp = PromptTemplate(template="System instraction : {sys_message}\n{hum_message}",
                          input_variables=['sys_message', 'hum_message'])
    
    prompt = temp.invoke(
        {
            'sys_message': sys_message.content,
            'hum_message': hum_message.content
        }
    )
    # print(prompt)
    return str(prompt)