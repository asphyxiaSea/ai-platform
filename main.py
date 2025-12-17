from fastapi import FastAPI
from router.ollama import router as ollama_router

app = FastAPI(title="Ollama API")

app.include_router(ollama_router)