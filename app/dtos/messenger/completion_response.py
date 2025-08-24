from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class CompletionResponse(BaseModel):
    llm_response: str
    message_id: int
    created_at: datetime

class MessageContext(BaseModel):
    role: str
    content: str
    created_at: datetime

class MessagesListResponse(BaseModel):
    chat_id: int
    messages: List[MessageContext]
    total_messages: int
