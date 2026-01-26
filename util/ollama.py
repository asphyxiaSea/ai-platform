from pydantic import BaseModel
from fastapi import HTTPException
import httpx


async def ollama_format_output(
    *,
    model: str,
    schema: type[BaseModel],
    messages: list[dict],
    temperature: float,
) -> BaseModel:

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
        # Ollama 强束缚
        "format": schema.model_json_schema(),
    }

    try:
        async with httpx.AsyncClient(timeout=100.0) as client:
            resp = await client.post("http://localhost:8001/api/chat", json=payload)
            resp.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError):
        raise HTTPException(502, "推理超时或 Ollama 服务异常")

    data = resp.json()
    content = data.get("message", {}).get("content", "")

    # ⭐ 核心防护：不要把空字符串交给 pydantic
    if not content or not content.strip():
        return schema.model_validate({})

    return schema.model_validate_json(content)


async def ollama_output(
    *,
    model: str,
    messages: list[dict],
    temperature: float,
) -> str:

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": temperature,
    }

    try:
        async with httpx.AsyncClient(timeout=200.0) as client:
            resp = await client.post("http://localhost:8001/api/chat", json=payload)
            resp.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError):
        raise HTTPException(502, "推理超时或 Ollama 服务异常")

    return resp.json()["message"]["content"]