# API de Messenger - Documentación y Ejemplos

## 🚀 Endpoints Disponibles

### 1. **POST** `/api/v1/messenger/completion/{chat_id}`
**Enviar mensaje del usuario al LLM y obtener respuesta**

#### Request Body:
```json
{
  "message": "¿Puedes explicarme qué es Python?"
}
```

#### Response:
```json
{
  "status": "success",
  "message": "Completion processed successfully",
  "data": {
    "llm_response": "Python es un lenguaje de programación de alto nivel...",
    "message_id": 15,
    "created_at": "2025-08-24T05:30:00.123456"
  },
  "timestamp": "2025-08-24T05:30:00.123456"
}
```

#### Flujo interno:
1. ✅ Verifica que el chat existe
2. ✅ Obtiene el contexto anterior del chat (últimos 20 mensajes)
3. ✅ Agrega el nuevo mensaje del usuario al contexto
4. ✅ Envía el contexto completo a LM Studio
5. ✅ Guarda el mensaje del usuario en la BD
6. ✅ Guarda la respuesta del LLM en la BD
7. ✅ Retorna la respuesta del LLM

---

### 2. **GET** `/api/v1/messenger/registers/{chat_id}`
**Obtener todos los mensajes de un chat**

#### Response:
```json
{
  "status": "success",
  "message": "Chat messages retrieved successfully",
  "data": {
    "chat_id": 1,
    "messages": [
      {
        "role": "user",
        "content": "Hola, ¿cómo estás?",
        "created_at": "2025-08-24T05:25:00.123456"
      },
      {
        "role": "assistant",
        "content": "¡Hola! Estoy muy bien, gracias por preguntar.",
        "created_at": "2025-08-24T05:25:05.123456"
      },
      {
        "role": "user",
        "content": "¿Puedes explicarme qué es Python?",
        "created_at": "2025-08-24T05:30:00.123456"
      },
      {
        "role": "assistant",
        "content": "Python es un lenguaje de programación...",
        "created_at": "2025-08-24T05:30:05.123456"
      }
    ],
    "total_messages": 4
  },
  "timestamp": "2025-08-24T05:30:10.123456"
}
```

---

### 3. **PUT** `/api/v1/messenger/update/{llm_message_id}`
**Actualizar la respuesta del LLM y opcionalmente el mensaje del usuario**

#### Parámetros:
- `llm_message_id`: ID del mensaje del LLM que se quiere actualizar

#### Request Body (new_message es opcional):
```json
{
  "new_message": "Mejor explícame qué es JavaScript"
}
```

#### Request Body (sin new_message - reutiliza la pregunta anterior):
```json
{
}
```

#### Response:
```json
{
  "status": "success",
  "message": "Completion updated successfully",
  "data": {
    "llm_response": "JavaScript es un lenguaje de programación interpretado...",
    "message_id": 15,
    "created_at": "2025-08-24T05:35:00.123456"
  },
  "timestamp": "2025-08-24T05:35:00.123456"
}
```

#### Flujo interno actualizado:
1. ✅ Encuentra el mensaje del LLM por ID
2. ✅ Obtiene el mensaje del usuario asociado (par user-llm)
3. ✅ Si `new_message` se proporciona, lo usa como nueva pregunta
4. ✅ Si `new_message` es null, reutiliza la pregunta anterior del usuario
5. ✅ Obtiene el contexto previo (sin el par actual)
6. ✅ Envía el contexto actualizado a LM Studio
7. ✅ Actualiza el mensaje del usuario solo si se proporcionó `new_message`
8. ✅ Actualiza la respuesta del LLM con la nueva respuesta

---

## 🔧 Configuración Requerida

### Variables de entorno (.env):
```properties
LM_STUDIO_URL=http://127.0.0.1:1234
LM_STUDIO_MODEL=qwen/qwen3-8b
```

### LM Studio debe estar ejecutándose:
```bash
# Asegúrate de que LM Studio esté corriendo en el puerto 1234
# con el modelo qwen/qwen3-8b cargado
```

---

## 📝 Ejemplos de Uso con curl

### 1. Enviar mensaje al LLM:
```bash
curl -X POST "http://localhost:8000/api/v1/messenger/completion/1" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuáles son las ventajas de usar Python?"
  }'
```

### 2. Obtener historial del chat:
```bash
curl -X GET "http://localhost:8000/api/v1/messenger/registers/1"
```

### 3. Actualizar respuesta del LLM (con nuevo mensaje):
```bash
curl -X PUT "http://localhost:8000/api/v1/messenger/update/15" \
  -H "Content-Type: application/json" \
  -d '{
    "new_message": "Mejor cuéntame sobre las desventajas de Python"
  }'
```

### 4. Actualizar respuesta del LLM (reutilizando pregunta anterior):
```bash
curl -X PUT "http://localhost:8000/api/v1/messenger/update/15" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 🚨 Manejo de Errores

### Chat no encontrado (404):
```json
{
  "status_code": 404,
  "message": "Chat not found",
  "timestamp": "2025-08-24T05:30:00.123456"
}
```

### Error de comunicación con LLM (500):
```json
{
  "status_code": 500,
  "message": "Error communicating with LLM: Connection refused",
  "timestamp": "2025-08-24T05:30:00.123456"
}
```

### Mensaje no encontrado (404):
```json
{
  "status_code": 404,
  "message": "Message not found",
  "timestamp": "2025-08-24T05:30:00.123456"
}
```

---

## 🔄 Flujo Completo de Conversación

### Paso 1: Crear un chat
```bash
curl -X POST "http://localhost:8000/api/v1/chats/create" \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi chat con Python"}'
```

### Paso 2: Enviar primer mensaje
```bash
curl -X POST "http://localhost:8000/api/v1/messenger/completion/1" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿puedes ayudarme a aprender Python?"}'
```

### Paso 3: Continuar conversación
```bash
curl -X POST "http://localhost:8000/api/v1/messenger/completion/1" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son los tipos de datos básicos en Python?"}'
```

### Paso 4: Ver historial completo
```bash
curl -X GET "http://localhost:8000/api/v1/messenger/registers/1"
```

---

## 🎯 Características Principales

- ✅ **Contexto Conversacional**: Mantiene memoria de la conversación
- ✅ **Integración con LM Studio**: Comunicación directa con la API
- ✅ **Persistencia en BD**: Todos los mensajes se guardan automáticamente
- ✅ **Actualización de Respuestas**: Permite modificar respuestas del LLM
- ✅ **Manejo de Errores**: Respuestas consistentes y descriptivas
- ✅ **Formato OpenAI Compatible**: Usa roles "user" y "assistant"
