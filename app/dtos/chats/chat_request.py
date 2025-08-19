from pydantic import BaseModel
from typing import Optional

class ChatCreateRequest(BaseModel):
    name: str

class ChatUpdateRequest(BaseModel):
    name: str
