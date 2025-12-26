from fastapi import FastAPI
import uvicorn
from router.chat import router as chat_router

app = FastAPI(title="Ollama API")

app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )