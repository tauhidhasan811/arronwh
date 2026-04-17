from typing import List, Dict
from src.config.config_chat_model import ChatModels
from src.tools.database_tools import GetAllData
from src.services.prompt_templete import Prompt
from collections.abc import AsyncIterable

class AgenController:
    def __init__(self):
        self.agent = ChatModels().GetChatModel()
    

    def __call_agent(self, prompt):
        response = self.agent.invoke(prompt)
        return response
    
    def __get_tools_data(self, tools: List) -> Dict:


        all_tools_data = {}
        tools_data = []
        tools_name = []
        for tool in tools:
            name = tool['name']
            tools_name.append(name)
            data = {'tool_name': name}
            args = tool['args']['body']
            tool_result = GetAllData.invoke(args)
            data['tool_result': tool_result]
            tools_data.append(data)
        all_tools_data['names'] = tools_name
        all_tools_data['datas'] = tools_data
        return all_tools_data



    def __get_agent_response(self, prompt):
        response = self.__call_agent(prompt=prompt)

        have_tools = False
        tools_data = []
        tools = response.tool_calls
        if tools:
            have_tools = True
            tools_data = tools_data.extend(self.__get_tools_data(tools=tools))
        content = response.content

        return have_tools, content, tools_data
    
    async def get_response(self, user_query, previous_chat) -> AsyncIterable['str']:
        prompt = Prompt(user_query=user_query, previous_chat=previous_chat)

        
