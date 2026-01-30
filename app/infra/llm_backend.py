from __future__ import annotations

import asyncio
from typing import Any, List, cast

import httpx
from openai import OpenAI
from pydantic import BaseModel

from app.domain.errors import ExternalServiceError


# Same external LLM service, two structured-output styles.
OLLAMA_CHAT_URL = "http://localhost:8001/api/chat"
OPENAI_BASE_URL = "http://localhost:8001/v1"
OPENAI_API_KEY = "ollama"


def _get_openai_client() -> OpenAI:
    return OpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_API_KEY,
    )


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
            resp = await client.post(OLLAMA_CHAT_URL, json=payload)
            resp.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise ExternalServiceError(
            message="推理超时或 Ollama 服务异常",
            detail=str(exc),
        ) from exc

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
            resp = await client.post(OLLAMA_CHAT_URL, json=payload)
            resp.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        raise ExternalServiceError(
            message="推理超时或 Ollama 服务异常",
            detail=str(exc),
        ) from exc

    return resp.json()["message"]["content"]


async def openai_structure_output(
    *,
    model: str,
    schema: type[BaseModel],
    messages: List[dict],
    temperature: float,
) -> BaseModel:
    """Async wrapper for OpenAI-compatible client's structured outputs parsing.

    The underlying SDK call is synchronous; run it in a thread via `asyncio.to_thread`.
    """

    client = _get_openai_client()

    def _sync_call() -> Any:
        completion = client.chat.completions.parse(
            model=model,
            messages=cast(Any, messages),
            temperature=temperature,
            response_format=schema,
        )
        msg = completion.choices[0].message
        if getattr(msg, "parsed", None) is not None:
            return msg.parsed
        raise ValueError("Structured Outputs 解析失败,parsed 为空")

    result = await asyncio.to_thread(_sync_call)
    return cast(BaseModel, result)


async def openai_raw_output(
    *,
    model: str,
    messages: List[dict],
    temperature: float,
) -> str:
    """Return raw text content from OpenAI-compatible client asynchronously."""

    client = _get_openai_client()

    def _sync_call() -> Any:
        completion = client.chat.completions.create(
            model=model,
            messages=cast(Any, messages),
            temperature=temperature,
        )
        msg = completion.choices[0].message
        if isinstance(msg, dict):
            content = msg.get("content")
        else:
            content = getattr(msg, "content", None) or getattr(msg, "text", None)
        return content

    result = await asyncio.to_thread(_sync_call)
    return cast(str, result)
