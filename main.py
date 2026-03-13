from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.api.router.files_parse_router import router as files_parse_router
from app.api.router.voice_transcribe_router import router as voice_transcribe_router
from app.api.router.llm_router import router as llm_router
from app.api.router.sensitive_filter_router import router as sensitive_filter_router
from app.api.router.sam3_router import router as sam3_router
from app.domain.errors import AppError

app = FastAPI(title="ai platform")


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "detail": exc.detail,
            }
        },
    )

app.include_router(files_parse_router, prefix="/ai-platform")
app.include_router(voice_transcribe_router, prefix="/ai-platform")
app.include_router(llm_router, prefix="/ai-platform")
app.include_router(sensitive_filter_router, prefix="/ai-platform")
app.include_router(sam3_router, prefix="/ai-platform")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )