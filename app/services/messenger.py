from sqlalchemy.orm import Session
from app.repositories.messages import MessageRepository
from app.repositories.chats import ChatRepository
from app.providers.llm_studio_api import lm_studio_provider
from app.dtos.messenger.completion_request import CompletionRequest, UpdateCompletionRequest
from app.dtos.messenger.completion_response import CompletionResponse, MessagesListResponse, MessageContext
from typing import Optional
import asyncio

class CompletionService:
    
    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)
        self.chat_repository = ChatRepository(db)
    
    async def process_completion(self, chat_id: int, request: CompletionRequest) -> CompletionResponse:
        """
        Procesar una completion: obtener contexto, enviar a LLM, guardar mensajes
        """
        # Verificar que el chat existe
        chat = self.chat_repository.get_chat_by_id(chat_id)
        if not chat:
            raise ValueError("Chat not found")
        
        # 1. Obtener contexto anterior del chat
        context = self.message_repository.get_chat_context_for_llm(chat_id)
        
        # 2. Agregar el nuevo mensaje del usuario al contexto
        context.append({
            "role": "user",
            "content": request.message
        })
        
        # 3. Enviar al LLM
        try:
            llm_response = await lm_studio_provider.chat_completion(
                messages=context,
                system_message="Eres un asistente inteligente y útil. Responde de manera clara y concisa.",
                temperature=0.7,
                max_tokens=-1,
                stream=False
            )
            
            # Extraer la respuesta del LLM
            llm_content = llm_response['choices'][0]['message']['content']
            
        except Exception as e:
            raise Exception(f"Error communicating with LLM: {str(e)}")
        
        # 4. Guardar los mensajes en la base de datos
        try:
            # Guardar mensaje del usuario
            self.message_repository.create_message(chat_id, "user", request.message)
            
            # Guardar respuesta del LLM
            llm_message = self.message_repository.create_message(chat_id, "llm", llm_content)
            
            return CompletionResponse(
                llm_response=llm_content,
                message_id=llm_message.id,
                created_at=llm_message.created_at
            )
            
        except Exception as e:
            raise Exception(f"Error saving messages: {str(e)}")
    
    def get_chat_messages(self, chat_id: int) -> MessagesListResponse:
        """
        Obtener todos los mensajes de un chat en formato de contexto
        """
        # Verificar que el chat existe
        chat = self.chat_repository.get_chat_by_id(chat_id)
        if not chat:
            raise ValueError("Chat not found")
        
        # Obtener todos los mensajes
        messages = self.message_repository.get_all_messages_by_chat_id(chat_id)
        
        # Convertir a formato de respuesta
        message_contexts = []
        for message in messages:
            role = "assistant" if message.sender == "llm" else "user"
            message_contexts.append(MessageContext(
                role=role,
                content=message.content,
                created_at=message.created_at
            ))
        
        return MessagesListResponse(
            chat_id=chat_id,
            messages=message_contexts,
            total_messages=len(message_contexts)
        )
    
    async def update_completion(self, chat_id: int, new_message: Optional[str] = None) -> CompletionResponse:
        """
        Actualizar la respuesta del LLM del último par de mensajes de un chat.
        Si new_message es proporcionado, actualiza también el mensaje del usuario.
        """
        # 1. Verificar que el chat existe
        chat = self.chat_repository.get_chat_by_id(chat_id)
        if not chat:
            raise ValueError("Chat not found")
        
        # 2. Obtener el último par de mensajes (user, llm)
        user_message, llm_message = self.message_repository.get_last_two_messages(chat_id)
        
        if not llm_message or not user_message:
            raise ValueError("No message pair found in chat")
        
        # 3. Determinar qué mensaje del usuario usar
        user_content = new_message if new_message is not None else user_message.content
        
        # 4. Obtener contexto previo (sin incluir el par actual user-llm)
        # Para simplificar, obtenemos el contexto completo y removemos los últimos 2 mensajes
        full_context = self.message_repository.get_chat_context_for_llm(chat_id)
        
        # Remover los últimos 2 mensajes (user y assistant del par actual) si existen
        context = full_context[:-2] if len(full_context) >= 2 else []
        
        # 5. Agregar el mensaje del usuario (nuevo o reutilizado)
        context.append({
            "role": "user",
            "content": user_content
        })
        
        # 6. Enviar al LLM
        try:
            llm_response = await lm_studio_provider.chat_completion(
                messages=context,
                system_message="Eres un asistente inteligente y útil. Responde de manera clara y concisa.",
                temperature=0.7,
                max_tokens=-1,
                stream=False
            )
            
            llm_content = llm_response['choices'][0]['message']['content']
            
        except Exception as e:
            raise Exception(f"Error communicating with LLM: {str(e)}")
        
        # 7. Actualizar los mensajes en la base de datos
        try:
            updated_user, updated_llm = self.message_repository.update_last_message_pair(
                chat_id,
                user_content if new_message is not None else None,  # Solo actualizar user si hay new_message
                llm_content
            )
            
            if not updated_llm:
                raise Exception("Failed to update messages")
            
            return CompletionResponse(
                llm_response=llm_content,
                message_id=updated_llm.id,
                created_at=updated_llm.created_at
            )
            
        except Exception as e:
            raise Exception(f"Error updating messages: {str(e)}")
