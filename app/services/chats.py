from sqlalchemy.orm import Session
from app.repositories.chats import ChatRepository
from app.dtos.chats.chat_request import ChatCreateRequest, ChatUpdateRequest
from app.dtos.chats.chat_response import ChatResponse, ChatListResponse
from app.utils.response_mapper import PaginationMeta
from typing import List, Optional, Tuple

class ChatService:
    
    def __init__(self, db: Session):
        self.chat_repository = ChatRepository(db)
    
    def create_chat(self, request: ChatCreateRequest) -> ChatResponse:
        """Crear un nuevo chat"""
        chat = self.chat_repository.create_chat(request.name)
        return ChatResponse.model_validate(chat)
    
    def get_chat_by_id(self, chat_id: int) -> Optional[ChatResponse]:
        """Obtener un chat por ID"""
        chat = self.chat_repository.get_chat_by_id(chat_id)
        if chat:
            return ChatResponse.model_validate(chat)
        return None
    
    def update_chat(self, chat_id: int, request: ChatUpdateRequest) -> Optional[ChatResponse]:
        """Actualizar un chat"""
        chat = self.chat_repository.update_chat(chat_id, request.name)
        if chat:
            return ChatResponse.model_validate(chat)
        return None
    
    def delete_chat(self, chat_id: int) -> bool:
        """Eliminar un chat"""
        return self.chat_repository.delete_chat(chat_id)
    
    def get_all_chats_paginated(self, page: int = 1, items_per_page: int = 16) -> Tuple[List[ChatListResponse], PaginationMeta]:
        """Obtener todos los chats con paginación"""
        chats_data, total_items = self.chat_repository.get_all_chats_paginated(page, items_per_page)
        
        chats = [
            ChatListResponse(
                id=chat.id,
                title=chat.title,
                created_at=chat.created_at,
                message_count=chat.message_count
            )
            for chat in chats_data
        ]
        
        pagination = PaginationMeta(page, total_items, items_per_page)
        return chats, pagination