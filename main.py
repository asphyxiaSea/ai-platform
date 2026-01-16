from fastapi import FastAPI
import uvicorn
from router.files_extract import router as files_extract_router

app = FastAPI(title="ai platform")

app.include_router(files_extract_router,prefix="/ai-platform")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )