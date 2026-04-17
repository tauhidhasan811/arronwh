from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.schemas.chat_body import Chatbody
from src.services.data_processor import DataProcessor

data_processor = DataProcessor()

router = APIRouter(prefix='/api/ai', tags=['Chat With AI'])

@router.post('/chatbot')
async def chat_with_ai(body: Chatbody):
    previous_chat = body.previous_chat
    selected_chat = data_processor.process_previous_history(previous_data=previous_chat)
    user_query = body.user_query
    print(type(previous_chat))
    response = JSONResponse(
        status_code=200,
        content={
            'status': True,
            'status_code': 200,
            'response': selected_chat
        }
    )
    return response

    # return body
