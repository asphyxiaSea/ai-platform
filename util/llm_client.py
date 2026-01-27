from typing import Any
import os
from pydantic import BaseModel
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from .ollama import ollama_format_output, ollama_output
from .openai import openai_structure_output, openai_raw_output


DEFAULT_BACKEND = os.environ.get("LLM_BACKEND", "ollama")


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

    if backend == "ollama":
        return await _ollama_format_with_retry(model=model, schema=schema, messages=messages, temperature=temperature)

    if backend == "openai":
        return await _openai_structure_with_retry(model=model, schema=schema, messages=messages, temperature=temperature)

    raise ValueError(f"Unknown LLM backend: {backend}")


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
    if backend == "ollama":
        return await _ollama_raw_with_retry(model=model, messages=messages, temperature=temperature)

    if backend == "openai":
        return await _openai_raw_with_retry(model=model, messages=messages, temperature=temperature)

    raise ValueError(f"Unknown LLM backend: {backend}")
