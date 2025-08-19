from app.conf.db import engine
from sqlalchemy import text  # <- importante

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT @@VERSION"))  # <- usar text()
            for row in result:
                print("Conexión exitosa. SQL Server versión:", row[0])
    except Exception as e:
        print("Error de conexión:", e)

if __name__ == "__main__":
    test_connection()
