from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
