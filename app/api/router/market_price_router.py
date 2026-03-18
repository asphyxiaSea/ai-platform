from __future__ import annotations

from fastapi import APIRouter, Query

from app.domain.errors import InvalidRequestError
from app.service.market_price_service import market_price_service

router = APIRouter(prefix="/market", tags=["market price"])


@router.get("/price")
async def get_market_price(url: str = Query(..., description="行情页面 URL")):
    if not (url.startswith("http://") or url.startswith("https://")):
        raise InvalidRequestError(message="url 必须是 http 或 https 开头")

    return await market_price_service(url=url)
