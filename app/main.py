from fastapi import FastAPI
from app.conf.db import engine
from app.routes.chats import router as chats_router
from app.routes.messenger import router as messenger_router
from sqlalchemy import text

app = FastAPI(title="Chat with Qwen")

# Incluir rutas
app.include_router(chats_router)
app.include_router(messenger_router)
\
@app.get("/")
def root():
    return {"message": "Hola, FastAPI está vivo 🚀"}

@app.on_event("startup")
def startup_event():
    # probar conexión a DB
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Conexión a DB exitosa y segura")
    except Exception as e:
        print("Error de conexión a DB:", e)
    
    # crear tablas automáticamente
    from app.entities import chats, messages 
    from app.conf.db import Base
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas en la DB si no existían")
