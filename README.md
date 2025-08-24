# 🚀 Chat with Qwen API

API hecha con **FastAPI** + **SQL Server** + **LM Studio (Qwen)**.  

---

## ⚙️ Requisitos
- Python 3.11+  
- SQL Server  
- LM Studio corriendo con modelo Qwen  

---

## 📦 Instalación
```bash
git clone https://github.com/isTaylor789/chat_with_qwen.git
cd chat_with_qwen/chat_with_qwen_api
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```


🔑 Variables de Entorno (.env)
DATABASE_URL=mssql+pymssql://sa:TuPass123!@localhost:1433/master
LM_STUDIO_URL=http://127.0.0.1:1234
LM_STUDIO_MODEL=qwen/qwen3-8b


▶️ Ejecución
 ```bash
uvicorn app.main:app --reload --port 3555
Swagger UI → http://localhost:3555/docs

ReDoc → http://localhost:3555/redoc
```
