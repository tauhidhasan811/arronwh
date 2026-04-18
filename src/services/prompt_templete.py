from typing import List, Dict
from langchain_core.prompts import PromptTemplate
from langchain.messages import HumanMessage, SystemMessage, AIMessage

class PromptGenerator:

    @staticmethod   
    def GeneralPrompt(user_query, previous_chat: List[Dict]):
        sys_message = SystemMessage(
            content = (
                "You are an assistant for a boiler company that sells boilers, controllers, and related products. "
                "Your responsibility is to answer customer queries about these products and use available tools when necessary. "
                "Provide accurate, concise, and relevant answers. "
                "Do not hallucinate or make up information. "
                "If the question is outside the scope of boilers, controllers, or related products, politely respond with a brief apology and state that you can only assist with company-related products."
            )
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
    
    @staticmethod   
    def ToolsPrompt(user_query, tools_data: List[Dict]):
        sys_message = SystemMessage(
            content=(f"You are a assiestent of the boiler company"
                     "your task analysis tools data based on user query.")
        )

        hum_message = HumanMessage(
            content= f'Current user Query: {user_query} \n\n Tools data : {tools_data}'
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
    