from typing import List, Dict
from langchain_core.prompts import PromptTemplate
from langchain.messages import HumanMessage, SystemMessage, AIMessage

class PromptGenerator:

    @staticmethod
    def output_templete():
        # Fixed string formatting and removed unnecessary concatenation
        return (
            "text will be short do not describe so long."
            "response use proper html tag like <p>, <tb>, <tr>, <ul>, <li>, bold , italic "
            "do not use h1 or h2 like big tag"
        )

    @staticmethod   
    def GeneralPrompt(user_query, relevent_info, previous_chat: List[Dict]):
        sys_message = SystemMessage(
            content=(
                "You are an assistant for a boiler company that sells boilers, boiler controllers, and related products. "
                "Your responsibility is to answer customer queries about these products and use available tools when necessary. "
                "Provide accurate, concise, and relevant answers. "
                "text will be short do not describe so long."
                "Do not hallucinate or make up information. "
                "If the question is outside the scope of boilers, boiler controllers, or related products, politely respond with a brief apology and state that you can only assist with company-related products. "
                f"follow this template {PromptGenerator.output_templete()}"
            )
        )

        hum_message = HumanMessage(
            content=f'Current user Query: {user_query} \n\nRelevant information from RAG: {relevent_info} Previous Chat: {previous_chat}'
        )
        
        temp = PromptTemplate(template="System instruction: {sys_message}\n{hum_message}",
                             input_variables=['sys_message', 'hum_message'])
        
        prompt = temp.invoke(
            {
                'sys_message': sys_message.content,
                'hum_message': hum_message.content
            }
        )
        return str(prompt)

    @staticmethod   
    def ToolsPrompt(user_query, tools_data: List[Dict]):
        sys_message = SystemMessage(
            content=(
                "You are an assistant of the boiler company. "
                "Your task is to analyze tools data based on user query."
                "text will be short do not describe so long."
            # f"follow this template {PromptGenerator.output_templete()}"
            )
        )

        hum_message = HumanMessage(
            content=f'Current user Query: {user_query} \n\nTools data: {tools_data}'
        )
        
        temp = PromptTemplate(template="System instruction: {sys_message}\n{hum_message}",
                             input_variables=['sys_message', 'hum_message'])
        
        prompt = temp.invoke(
            {
                'sys_message': sys_message.content,
                'hum_message': hum_message.content
            }
        )
        return str(prompt)