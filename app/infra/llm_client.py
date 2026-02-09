from __future__ import annotations

import asyncio
from typing import Any, List, cast

import httpx
from openai import OpenAI
from pydantic import BaseModel
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from app.domain.errors import AppError, ExternalServiceError
from app.infra.url_config import OLLAMA_LLM_URL, OPENAI_LLM_URL


DEFAULT_BACKEND = "ollama"


# Same external LLM service, two structured-output styles.


def _get_openai_client() -> OpenAI:
    return OpenAI(
        base_url=OPENAI_LLM_URL,
        api_key="ollama",
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
            resp = await client.post(OLLAMA_LLM_URL, json=payload)
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
            resp = await client.post(OLLAMA_LLM_URL, json=payload)
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


# --- retry wrappers ---

# Retry Ollama calls on httpx network/HTTP status errors
@retry(
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    wait=wait_exponential(min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def _ollama_format_with_retry(model: str, schema: type[BaseModel], messages: list[dict], temperature: float) -> BaseModel:
    return await ollama_format_output(model=model, schema=schema, messages=messages, temperature=temperature)


@retry(
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
    wait=wait_exponential(min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def _ollama_raw_with_retry(model: str, messages: list[dict], temperature: float) -> str:
    return await ollama_output(model=model, messages=messages, temperature=temperature)


# Retry OpenAI wrapper on generic exceptions (SDK/network); conservative 3 attempts
@retry(
    retry=retry_if_exception_type(Exception),
    wait=wait_exponential(min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def _openai_structure_with_retry(model: str, schema: type[BaseModel], messages: list[dict], temperature: float) -> BaseModel:
    return await openai_structure_output(model=model, schema=schema, messages=messages, temperature=temperature)


@retry(
    retry=retry_if_exception_type(Exception),
    wait=wait_exponential(min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def _openai_raw_with_retry(model: str, messages: list[dict], temperature: float) -> str:
    return await openai_raw_output(model=model, messages=messages, temperature=temperature)


async def structured_output(
    *,
    model: str,
    schema: type[BaseModel],
    messages: list[dict],
    temperature: float,
    backend: str | None = None,
) -> BaseModel:
    """Return a pydantic model parsed from the model's structured output.

    backend: 'ollama' or 'openai'. If None, uses `LLM_BACKEND` env or defaults to 'ollama'.
    """
    if backend is None:
        backend = DEFAULT_BACKEND

    backend = backend.lower()

    try:
        if backend == "openai":
            return await _openai_structure_with_retry(model=model, schema=schema, messages=messages, temperature=temperature)

        return await _ollama_format_with_retry(model=model, schema=schema, messages=messages, temperature=temperature)
    except AppError:
        raise
    except Exception as exc:
        raise ExternalServiceError(message="LLM 调用失败", detail=str(exc)) from exc


async def raw_output(
    *,
    model: str,
    messages: list[dict],
    temperature: float,
    backend: str | None = None,
) -> str:
    """Return raw text output from the LLM backend."""
    if backend is None:
        backend = DEFAULT_BACKEND

    backend = backend.lower()
    try:
        if backend == "openai":
            return await _openai_raw_with_retry(model=model, messages=messages, temperature=temperature)

        return await _ollama_raw_with_retry(model=model, messages=messages, temperature=temperature)
    except AppError:
        raise
    except Exception as exc:
        raise ExternalServiceError(message="LLM 调用失败", detail=str(exc)) from exc
