from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from api.schemas.chat_body import Chatbody
from src.services.data_processor import DataProcessor
# from src.services.prompt_templete import Prompt
from src.controller.agent_controller import AgenController
from src.services.rag_knowledge import RagKnowledge
from src.config.config_embedding_model import Embedder


embedder = Embedder().hugg_sentence_embedder()
rag = RagKnowledge(embedding_model=embedder)
data_processor = DataProcessor()

router = APIRouter(prefix='/api/ai', tags=['Chat With AI'])

@router.post('/chatbot')
async def chat_with_ai(body: Chatbody):
    previous_chat = body.previous_chat
    selected_chat = data_processor.process_previous_history(previous_data=previous_chat)
    user_query = body.user_query
    relevent_info = rag.retrive_chunk(user_query)
    print(relevent_info)
    agent_controller = AgenController()

    return StreamingResponse(agent_controller.get_response(user_query=user_query, 
                                                           relevent_info = relevent_info, 
                                                           previous_chat=previous_chat), 
                                                           media_type='text/event-stream')


    return message
