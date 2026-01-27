from openai import OpenAI
from pydantic import BaseModel
import asyncio
from typing import Any, List, cast

# 指向本地 Ollama 服务
client = OpenAI(
    base_url='http://localhost:8001/v1',
    api_key='ollama',
)


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
    # The SDK returns a Pydantic model-like object; cast to BaseModel for the type checker
    return cast(BaseModel, result)


async def openai_raw_output(*, model: str, messages: List[dict], temperature: float) -> str:
    """Return raw text content from OpenAI-compatible client asynchronously."""

    def _sync_call() -> Any:
        completion = client.chat.completions.create(
            model=model,
            messages=cast(Any, messages),
            temperature=temperature,
        )
        msg = completion.choices[0].message
        # message content may be attribute or dict key; handle both safely
        if isinstance(msg, dict):
            content = msg.get("content")
        else:
            content = getattr(msg, "content", None) or getattr(msg, "text", None)
        return content

    result = await asyncio.to_thread(_sync_call)
    return cast(str, result)

