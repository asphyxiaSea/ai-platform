from fastapi import FastAPI
import uvicorn
from router.multimodal import router as multimodal_router
from router.texts import router as texts_router
from router.combined import router as combined_router

app = FastAPI(title="Ollama API")

app.include_router(multimodal_router)
app.include_router(texts_router)
app.include_router(combined_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )