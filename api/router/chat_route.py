from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from api.schemas.chat_body import Chatbody
from src.services.data_processor import DataProcessor
# from src.services.prompt_templete import Prompt
from src.controller.agent_controller import AgenController

data_processor = DataProcessor()

router = APIRouter(prefix='/api/ai', tags=['Chat With AI'])

@router.post('/chatbot')
async def chat_with_ai(body: Chatbody):
    previous_chat = body.previous_chat
    selected_chat = data_processor.process_previous_history(previous_data=previous_chat)
    user_query = body.user_query
    agent_controller = AgenController()

    return StreamingResponse(agent_controller.get_response(user_query=user_query, previous_chat=previous_chat), media_type='text/plain')
    # prompt = Prompt(user_query, selected_chat)
    # print(type(previous_chat))
    # message = agent_controller.get_response(user_query=user_query, previous_chat=previous_chat)
    # response = JSONResponse(
    #     status_code=200,
    #     content={
    #         'status': True,
    #         'status_code': 200,
    #         'response': message
    #     }
    # )
    # return response

    return message
