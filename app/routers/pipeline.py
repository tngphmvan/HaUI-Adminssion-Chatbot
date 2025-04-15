"""
Chat API using streaming response
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.tracers.context import tracing_v2_enabled

from models.pipline import Pipline
from schemas.chat_model import ChatMessage

router = APIRouter()

@router.post("/chat")
async def chat_stream(request: ChatMessage):
    """API chat using streaming response"""
    with tracing_v2_enabled("ftu_chatbot"):
        return StreamingResponse(Pipline(
            collection_name=request.collection_name,
            system_prompt=request.system_prompt
        ).stream_rag_response(question=request.query, session_id=request.session_id), media_type="text/event-stream")
