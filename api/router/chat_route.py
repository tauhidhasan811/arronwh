from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.schemas.chat_body import Chatbody


router = APIRouter(prefix='/api/ai', tags=['Chat With AI'])

@router.post('/chatbot')
async def chat_with_ai(body: Chatbody):
    previous_chat = body.previous_chat
    user_query = body.user_query
    print(type(previous_chat))
    # response = JSONResponse(
    #     status_code=200,
    #     content={
    #         'status': True,
    #         'status_code': 200,
    #         'response': {
    #             "data": body,
    #                      'user_query': user_query}
    #     }
    # )
    # return response

    return body
