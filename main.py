from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.api.router.files_extract import router as files_extract_router
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

app.include_router(files_extract_router,prefix="/ai-platform")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )