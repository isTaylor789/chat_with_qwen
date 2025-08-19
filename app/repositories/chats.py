from sqlalchemy.orm import Session
from sqlalchemy import func
from app.entities.chats import Chat
from app.entities.messages import Message
from typing import List, Optional, Tuple

class ChatRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_chat(self, name: str) -> Chat:
        """Crear un nuevo chat"""
        chat = Chat(title=name)  # mapear name a title
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat
    
    def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        """Obtener un chat por ID con sus mensajes"""
        return self.db.query(Chat).filter(Chat.id == chat_id).first()
    
    def update_chat(self, chat_id: int, name: str) -> Optional[Chat]:
        """Actualizar el título de un chat"""
        chat = self.db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            chat.title = name  # mapear name a title
            self.db.commit()
            self.db.refresh(chat)
        return chat
    
    def delete_chat(self, chat_id: int) -> bool:
        """Eliminar un chat y sus mensajes asociados"""
        chat = self.db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            # Eliminar mensajes asociados primero
            self.db.query(Message).filter(Message.chat_id == chat_id).delete()
            # Eliminar el chat
            self.db.delete(chat)
            self.db.commit()
            return True
        return False
    
    def get_all_chats_paginated(self, page: int = 1, items_per_page: int = 16) -> Tuple[List[tuple], int]:
        """Obtener todos los chats con conteo de mensajes y paginación"""
        offset = (page - 1) * items_per_page
        
        # Obtener el total de chats
        total_chats = self.db.query(Chat).count()
        
        # Obtener los chats paginados
        chats = (
            self.db.query(
                Chat.id,
                Chat.title,
                Chat.created_at,
                func.count(Message.id).label('message_count')
            )
            .outerjoin(Message)
            .group_by(Chat.id, Chat.title, Chat.created_at)
            .order_by(Chat.created_at.desc())
            .offset(offset)
            .limit(items_per_page)
            .all()
        )
        
        return chats, total_chats