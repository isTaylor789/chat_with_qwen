from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.controllers.messenger import MessengerController
from app.dtos.messenger.completion_request import CompletionRequest
from app.conf.db import get_db
from typing import Dict, Optional

router = APIRouter(prefix="/api/v1/messenger", tags=["messenger"])

@router.post("/completion/{chat_id}")
async def process_completion(
    chat_id: int, 
    request: CompletionRequest, 
    db: Session = Depends(get_db)
) -> Dict:
    """Enviar mensaje del usuario al LLM y obtener respuesta"""
    return await MessengerController.process_completion(chat_id, request, db)

@router.get("/registers/{chat_id}")
def get_chat_registers(
    chat_id: int, 
    db: Session = Depends(get_db)
) -> Dict:
    """Obtener todos los mensajes de un chat"""
    return MessengerController.get_chat_registers(chat_id, db)

@router.put("/update/{chat_id}")
async def update_completion(
    chat_id: int, 
    new_message: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
) -> Dict:
    """Actualizar los últimos mensajes del chat (user-llm) con nuevo mensaje opcional"""
    return await MessengerController.update_completion(chat_id, new_message, db)
