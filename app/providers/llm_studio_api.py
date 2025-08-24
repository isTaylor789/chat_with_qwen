import httpx
import json
from typing import List, Dict, Optional, AsyncGenerator
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class LMStudioAPIProvider:
    """Proveedor para comunicarse con la API de LM Studio"""
    
    def __init__(self):
        self.base_url = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234")
        self.model = os.getenv("LM_STUDIO_MODEL", "qwen/qwen3-8b")
        self.timeout = httpx.Timeout(60.0)  # 60 segundos de timeout
    
    async def get_available_models(self) -> List[Dict]:
        """Obtener los modelos disponibles en LM Studio"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/v1/models")
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to LM Studio: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error from LM Studio: {e.response.status_code}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = -1,
        stream: bool = False,
        system_message: Optional[str] = None
    ) -> Dict:
        """
        Realizar una consulta de chat completion a LM Studio
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user|assistant", "content": "..."}]
            temperature: Temperatura para la generación (0.0 a 1.0)
            max_tokens: Número máximo de tokens (-1 para ilimitado)
            stream: Si debe hacer streaming o devolver respuesta completa
            system_message: Mensaje del sistema opcional
        """
        try:
            # Preparar mensajes
            formatted_messages = []
            
            # Agregar mensaje del sistema si se proporciona
            if system_message:
                formatted_messages.append({
                    "role": "system", 
                    "content": system_message
                })
            
            # Agregar mensajes del contexto
            formatted_messages.extend(messages)
            
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to LM Studio: {str(e)}")
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
            raise Exception(f"HTTP error from LM Studio: {e.response.status_code} - {error_detail}")
    
    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = -1,
        system_message: Optional[str] = None
    ) -> AsyncGenerator[Dict, None]:
        """
        Realizar una consulta de chat completion con streaming
        
        Args:
            messages: Lista de mensajes en formato [{"role": "user|assistant", "content": "..."}]
            temperature: Temperatura para la generación
            max_tokens: Número máximo de tokens
            system_message: Mensaje del sistema opcional
            
        Yields:
            Chunks de respuesta del streaming
        """
        try:
            # Preparar mensajes
            formatted_messages = []
            
            if system_message:
                formatted_messages.append({
                    "role": "system", 
                    "content": system_message
                })
            
            formatted_messages.extend(messages)
            
            payload = {
                "model": self.model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            # Las líneas de streaming vienen como "data: {...}"
                            if line.startswith("data: "):
                                data_str = line[6:]  # Remover "data: "
                                if data_str.strip() == "[DONE]":
                                    break
                                try:
                                    chunk = json.loads(data_str)
                                    yield chunk
                                except json.JSONDecodeError:
                                    continue
                                    
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to LM Studio: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error from LM Studio: {e.response.status_code}")
    
    async def simple_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = -1
    ) -> Dict:
        """
        Realizar una consulta simple de completion (no chat)
        
        Args:
            prompt: El prompt a completar
            temperature: Temperatura para la generación
            max_tokens: Número máximo de tokens
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to LM Studio: {str(e)}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error from LM Studio: {e.response.status_code}")

# Instancia global del proveedor
lm_studio_provider = LMStudioAPIProvider()
