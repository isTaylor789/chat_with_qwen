# Ejemplos de uso de Repository Messages y LM Studio Provider

## 🗄️ MessageRepository - Nueva función get_chat_context_for_llm()

### Propósito
Esta función obtiene el historial de mensajes de un chat en formato compatible con OpenAI/LM Studio para enviar como contexto al LLM.

### Uso
```python
from app.repositories.messages import MessageRepository
from app.conf.db import SessionLocal

# Crear instancia del repositorio
db = SessionLocal()
message_repo = MessageRepository(db)

# Obtener contexto del chat para el LLM (últimos 20 mensajes por defecto)
context = message_repo.get_chat_context_for_llm(chat_id=1, limit=20)

# El resultado será algo como:
# [
#     {"role": "user", "content": "Hola, ¿cómo estás?"},
#     {"role": "assistant", "content": "¡Hola! Estoy bien, gracias por preguntar."},
#     {"role": "user", "content": "¿Puedes ayudarme con Python?"},
#     {"role": "assistant", "content": "Por supuesto, estaré encantado de ayudarte."}
# ]
```

### Mapeo de roles
- `sender = "user"` → `role = "user"`
- `sender = "llm"` → `role = "assistant"`

## 🤖 LMStudioAPIProvider - Comunicación con LM Studio

### Funciones disponibles

#### 1. get_available_models()
```python
from app.providers.llm_studio_api import lm_studio_provider
import asyncio

async def check_models():
    models = await lm_studio_provider.get_available_models()
    print(models)

asyncio.run(check_models())
```

#### 2. chat_completion() - Respuesta completa
```python
async def chat_with_llm():
    messages = [
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ]
    
    response = await lm_studio_provider.chat_completion(
        messages=messages,
        system_message="Eres un asistente útil y amigable.",
        temperature=0.7,
        max_tokens=100,
        stream=False
    )
    
    print(response)
    # El contenido estará en: response['choices'][0]['message']['content']

asyncio.run(chat_with_llm())
```

#### 3. chat_completion_stream() - Streaming de respuesta
```python
async def chat_with_streaming():
    messages = [
        {"role": "user", "content": "Explícame qué es Python"}
    ]
    
    async for chunk in lm_studio_provider.chat_completion_stream(
        messages=messages,
        system_message="Eres un experto en programación.",
        temperature=0.7
    ):
        # Procesar cada chunk del streaming
        if 'choices' in chunk and len(chunk['choices']) > 0:
            delta = chunk['choices'][0].get('delta', {})
            if 'content' in delta:
                print(delta['content'], end='', flush=True)

asyncio.run(chat_with_streaming())
```

#### 4. simple_completion() - Completion simple
```python
async def simple_completion():
    response = await lm_studio_provider.simple_completion(
        prompt="El lenguaje de programación más popular es",
        temperature=0.5,
        max_tokens=50
    )
    
    print(response)

asyncio.run(simple_completion())
```

## 🔗 Uso combinado: Repository + Provider

### Ejemplo de flujo completo
```python
async def complete_chat_flow(chat_id: int, user_message: str):
    db = SessionLocal()
    try:
        # 1. Obtener contexto del chat
        message_repo = MessageRepository(db)
        context = message_repo.get_chat_context_for_llm(chat_id)
        
        # 2. Agregar el nuevo mensaje del usuario
        context.append({"role": "user", "content": user_message})
        
        # 3. Enviar a LM Studio
        response = await lm_studio_provider.chat_completion(
            messages=context,
            system_message="Eres un asistente inteligente y útil.",
            temperature=0.7
        )
        
        # 4. Extraer la respuesta del LLM
        llm_response = response['choices'][0]['message']['content']
        
        # 5. Guardar ambos mensajes en la BD
        message_repo.create_message(chat_id, "user", user_message)
        message_repo.create_message(chat_id, "llm", llm_response)
        
        db.commit()
        return llm_response
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
```

## ⚙️ Configuración en .env
```properties
LM_STUDIO_URL=http://127.0.0.1:1234
LM_STUDIO_MODEL=qwen/qwen3-8b
```

## 📋 Dependencias necesarias
Asegúrate de tener `httpx` instalado:
```bash
pip install httpx
```
