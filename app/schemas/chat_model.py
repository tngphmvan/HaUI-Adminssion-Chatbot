import uuid

from pydantic import BaseModel


class ChatMessage(BaseModel):
    query: str
    session_id: str = str(uuid.uuid4())
    collection_name: str
