from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.conf.db import get_db
from app.services.chats import ChatService
from app.dtos.chats.chat_request import ChatCreateRequest, ChatUpdateRequest
from app.dtos.chats.chat_response import ChatResponse, ChatListResponse
from app.utils.response_mapper import ResponseMapper, ErrorResponseMapper
from typing import List, Dict

class ChatController:
    
    @staticmethod
    def create_chat(request: ChatCreateRequest, db: Session = Depends(get_db)) -> Dict:
        """Crear un nuevo chat"""
        try:
            chat_service = ChatService(db)
            chat = chat_service.create_chat(request)
            return ResponseMapper.success("Chat created successfully", chat)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=ErrorResponseMapper.error(500, f"Error creating chat: {str(e)}")
            )
    
    @staticmethod
    def get_chat_by_id(chat_id: int, db: Session = Depends(get_db)) -> Dict:
        """Obtener un chat por ID"""
        try:
            chat_service = ChatService(db)
            chat = chat_service.get_chat_by_id(chat_id)
            if not chat:
                raise HTTPException(
                    status_code=404,
                    detail=ErrorResponseMapper.error(404, "Chat not found")
                )
            return ResponseMapper.success("Chat retrieved successfully", chat)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error retrieving chat: {str(e)}")
            )
    
    @staticmethod
    def update_chat(chat_id: int, request: ChatUpdateRequest, db: Session = Depends(get_db)) -> Dict:
        """Actualizar un chat"""
        try:
            chat_service = ChatService(db)
            chat = chat_service.update_chat(chat_id, request)
            if not chat:
                raise HTTPException(
                    status_code=404,
                    detail=ErrorResponseMapper.error(404, "Chat not found")
                )
            return ResponseMapper.success("Chat updated successfully", chat)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error updating chat: {str(e)}")
            )
    
    @staticmethod
    def delete_chat(chat_id: int, db: Session = Depends(get_db)) -> Dict:
        """Eliminar un chat"""
        try:
            chat_service = ChatService(db)
            success = chat_service.delete_chat(chat_id)
            if not success:
                raise HTTPException(
                    status_code=404,
                    detail=ErrorResponseMapper.error(404, "Chat not found")
                )
            return ResponseMapper.success("Chat deleted successfully", {"deleted": True})
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error deleting chat: {str(e)}")
            )
    
    @staticmethod
    def get_all_chats(page: int = Query(1, ge=1), db: Session = Depends(get_db)) -> Dict:
        """Obtener todos los chats con paginación"""
        try:
            chat_service = ChatService(db)
            chats, pagination = chat_service.get_all_chats_paginated(page)
            return ResponseMapper.success("Chats retrieved successfully", chats, pagination)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error retrieving chats: {str(e)}")
            )
