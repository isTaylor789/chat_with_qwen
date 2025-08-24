from pydantic import BaseModel
from typing import Optional

class CompletionRequest(BaseModel):
    message: str

class UpdateCompletionRequest(BaseModel):
    new_message: Optional[str] = None
