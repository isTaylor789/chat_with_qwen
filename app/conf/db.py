import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# cargar variables de entorno
load_dotenv()

# obtener URL de conexión
DATABASE_URL = os.getenv("DATABASE_URL")

# crear engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True, future=True)

# session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clase base para modelos
Base = declarative_base()

# función auxiliar para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
