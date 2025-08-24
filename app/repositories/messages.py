from sqlalchemy.orm import Session
from app.entities.messages import Message
from typing import List, Optional, Dict

class MessageRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_message(self, chat_id: int, sender: str, content: str) -> Message:
        """Crear un nuevo mensaje"""
        message = Message(chat_id=chat_id, sender=sender, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_chat_context_for_llm(self, chat_id: int, limit: int = 20) -> List[Dict[str, str]]:
        """Obtener el contexto del chat en formato para LLM"""
        messages = (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
            .all()
        )
        
        # Convertir a formato OpenAI compatible
        context = []
        for message in messages:
            # Mapear 'user' y 'llm' a 'user' y 'assistant' respectivamente
            role = "assistant" if message.sender == "llm" else "user"
            context.append({
                "role": role,
                "content": message.content
            })
        
        return context
    
    def get_all_messages_by_chat_id(self, chat_id: int) -> List[Message]:
        """Obtener todos los mensajes de un chat ordenados por fecha"""
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )
    
    def get_last_two_messages(self, chat_id: int) -> tuple[Optional[Message], Optional[Message]]:
        """
        Obtener los dos últimos mensajes de un chat.
        Retorna (user_last_message, llm_last_message)
        """
        # Obtener los dos últimos mensajes ordenados por fecha descendente
        last_messages = (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(2)
            .all()
        )
        
        if len(last_messages) < 2:
            return None, None
        
        # El primer mensaje debería ser del LLM (más reciente)
        # El segundo mensaje debería ser del usuario (anterior al LLM)
        llm_message = last_messages[0] if last_messages[0].sender == "llm" else None
        user_message = last_messages[1] if last_messages[1].sender == "user" else None
        
        # Si no coincide el patrón esperado, intentar encontrar el par correcto
        if not llm_message or not user_message:
            # Buscar el último mensaje del LLM
            llm_message = (
                self.db.query(Message)
                .filter(Message.chat_id == chat_id, Message.sender == "llm")
                .order_by(Message.created_at.desc())
                .first()
            )
            
            if llm_message:
                # Buscar el mensaje del usuario inmediatamente anterior
                user_message = (
                    self.db.query(Message)
                    .filter(
                        Message.chat_id == chat_id,
                        Message.sender == "user",
                        Message.created_at < llm_message.created_at
                    )
                    .order_by(Message.created_at.desc())
                    .first()
                )
        
        return user_message, llm_message
    
    def update_last_message_pair(self, chat_id: int, user_content: Optional[str] = None, llm_content: str = None) -> tuple[Optional[Message], Optional[Message]]:
        """
        Actualizar el último par de mensajes user-llm de un chat.
        Si user_content es None, solo actualiza el mensaje del LLM.
        """
        user_message, llm_message = self.get_last_two_messages(chat_id)
        
        if not user_message or not llm_message:
            return None, None
        
        # Actualizar mensaje del usuario si se proporciona nuevo contenido
        if user_content is not None:
            user_message.content = user_content
        
        # Actualizar mensaje del LLM
        if llm_content is not None:
            llm_message.content = llm_content
        
        self.db.commit()
        
        if user_content is not None:
            self.db.refresh(user_message)
        if llm_content is not None:
            self.db.refresh(llm_message)
        
        return user_message, llm_message