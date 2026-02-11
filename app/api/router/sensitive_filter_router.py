from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.service.sensitive_filter_service import filter_sensitive_text

router = APIRouter(prefix="/sensitive", tags=["sensitive_filter"])


@router.post("/filter", response_class=PlainTextResponse)
async def filter_text(text: str):
    return filter_sensitive_text(text)
