from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.conf.db import get_db
from app.services.messenger import CompletionService
from app.dtos.messenger.completion_request import CompletionRequest
from app.utils.response_mapper import ResponseMapper, ErrorResponseMapper
from typing import Dict, Optional
import asyncio

class MessengerController:
    
    @staticmethod
    async def process_completion(chat_id: int, request: CompletionRequest, db: Session = Depends(get_db)) -> Dict:
        """Procesar completion: enviar mensaje del usuario al LLM y obtener respuesta"""
        try:
            completion_service = CompletionService(db)
            result = await completion_service.process_completion(chat_id, request)
            return ResponseMapper.success("Completion processed successfully", result)
        except ValueError as ve:
            raise HTTPException(
                status_code=404,
                detail=ErrorResponseMapper.error(404, str(ve))
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error processing completion: {str(e)}")
            )
    
    @staticmethod
    def get_chat_registers(chat_id: int, db: Session = Depends(get_db)) -> Dict:
        """Obtener todos los mensajes de un chat (registros)"""
        try:
            completion_service = CompletionService(db)
            result = completion_service.get_chat_messages(chat_id)
            return ResponseMapper.success("Chat messages retrieved successfully", result)
        except ValueError as ve:
            raise HTTPException(
                status_code=404,
                detail=ErrorResponseMapper.error(404, str(ve))
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error retrieving messages: {str(e)}")
            )
    
    @staticmethod
    async def update_completion(chat_id: int, new_message: Optional[str], db: Session = Depends(get_db)) -> Dict:
        """Actualizar los últimos mensajes del chat (user-llm) con nuevo mensaje o reutilizar el anterior"""
        try:
            completion_service = CompletionService(db)
            result = await completion_service.update_completion(chat_id, new_message)
            return ResponseMapper.success("Completion updated successfully", result)
        except ValueError as ve:
            raise HTTPException(
                status_code=404,
                detail=ErrorResponseMapper.error(404, str(ve))
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=ErrorResponseMapper.error(500, f"Error updating completion: {str(e)}")
            )
