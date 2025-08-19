from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageResponse(BaseModel):
    id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ChatListResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True
