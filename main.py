from fastapi import FastAPI
import uvicorn
from router.ollama import router as ollama_router

app = FastAPI(title="Ollama API")

app.include_router(ollama_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003
    )