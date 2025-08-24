# Ejemplos de Respuestas con los Nuevos Mappers

## 🎯 ResponseMapper - Respuestas Exitosas (Actualizado)

### 1. Crear Chat - POST /api/v1/chats/create
```json
{
  "status": "success",
  "message": "Chat created successfully",
  "data": {
    "id": 1,
    "title": "Mi primer chat",
    "created_at": "2025-08-19T04:52:01.123456",
    "messages": []
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

### 2. Obtener Chat - GET /api/v1/chats/{chat_id}
```json
{
  "status": "success",
  "message": "Chat retrieved successfully",
  "data": {
    "id": 1,
    "title": "Mi primer chat",
    "created_at": "2025-08-19T04:52:01.123456",
    "messages": [
      {
        "id": 1,
        "sender": "user",
        "content": "Hola!",
        "created_at": "2025-08-19T04:52:01.123456"
      }
    ]
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

### 3. Listar Chats con Paginación - GET /api/v1/chats/list?page=1
```json
{
  "status": "success",
  "message": "Chats retrieved successfully",
  "data": [
    {
      "id": 1,
      "title": "Chat 1",
      "created_at": "2025-08-19T04:52:01.123456",
      "message_count": 5
    },
    {
      "id": 2,
      "title": "Chat 2",
      "created_at": "2025-08-19T04:52:01.123456",
      "message_count": 3
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_items": 25,
    "items_per_page": 16,
    "total_pages": 2,
    "has_next": true,
    "has_prev": false
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

## 📩 Endpoints de Mensajes - CRUD Completo

### 1. Crear Mensaje - POST /api/v1/messages/create
```json
{
  "status": "success",
  "message": "Message created successfully",
  "data": {
    "id": 1,
    "chat_id": 1,
    "sender": "user",
    "content": "Hola, ¿cómo estás?",
    "created_at": "2025-08-19T04:52:01.123456"
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

### 2. Obtener Mensaje - GET /api/v1/messages/{message_id}
```json
{
  "status": "success",
  "message": "Message retrieved successfully",
  "data": {
    "id": 1,
    "chat_id": 1,
    "sender": "user",
    "content": "Hola, ¿cómo estás?",
    "created_at": "2025-08-19T04:52:01.123456"
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

### 3. Actualizar Mensaje - PUT /api/v1/messages/{message_id}/update
```json
{
  "status": "success",
  "message": "Message updated successfully",
  "data": {
    "id": 1,
    "chat_id": 1,
    "sender": "user",
    "content": "Hola, ¿cómo te encuentras hoy?",
    "created_at": "2025-08-19T04:52:01.123456"
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

### 4. Eliminar Mensaje - DELETE /api/v1/messages/{message_id}/delete
```json
{
  "status": "success",
  "message": "Message deleted successfully",
  "data": {
    "deleted": true
  },
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

## ❌ ErrorResponseMapper - Respuestas de Error

### Chat No Encontrado - 404
```json
{
  "status_code": 404,
  "message": "Chat not found",
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

### Error Interno del Servidor - 500
```json
{
  "status_code": 500,
  "message": "Error creating chat: Database connection failed",
  "timestamp": "2025-08-19T04:52:01.123456"
}
```

## 📊 Características de la Paginación

- **items_per_page**: 16 (fijo)
- **current_page**: Página actual solicitada
- **total_items**: Total de elementos en la DB
- **total_pages**: Páginas totales calculadas
- **has_next**: Si hay página siguiente
- **has_prev**: Si hay página anterior

### Ejemplo de uso de paginación:
- Página 1: `GET /api/v1/chats/list?page=1`
- Página 2: `GET /api/v1/chats/list?page=2`
- Sin especificar (por defecto página 1): `GET /api/v1/chats/list`
