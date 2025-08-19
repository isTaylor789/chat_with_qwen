from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.controllers.chats import ChatController
from app.dtos.chats.chat_request import ChatCreateRequest, ChatUpdateRequest
from app.conf.db import get_db
from typing import Dict

router = APIRouter(prefix="/api/v1/chats", tags=["chats"])

@router.post("/create")
def create_chat(request: ChatCreateRequest, db: Session = Depends(get_db)) -> Dict:
    """Crear un nuevo chat"""
    return ChatController.create_chat(request, db)

@router.get("/list")
def get_all_chats(page: int = Query(1, ge=1), db: Session = Depends(get_db)) -> Dict:
    """Obtener todos los chats con paginación"""
    return ChatController.get_all_chats(page, db)

@router.get("/get/{chat_id}")
def get_chat_by_id(chat_id: int, db: Session = Depends(get_db)) -> Dict:
    """Obtener un chat por ID"""
    return ChatController.get_chat_by_id(chat_id, db)

@router.put("/update/{chat_id}")
def update_chat(chat_id: int, request: ChatUpdateRequest, db: Session = Depends(get_db)) -> Dict:
    """Actualizar un chat"""
    return ChatController.update_chat(chat_id, request, db)

@router.delete("/delete/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)) -> Dict:
    """Eliminar un chat"""
    return ChatController.delete_chat(chat_id, db)
