from pydantic import BaseModel
from typing import Literal

class MessageCreateRequest(BaseModel):
    chat_id: int
    sender: Literal["user", "llm"]
    content: str

class MessageUpdateRequest(BaseModel):
    content: str
