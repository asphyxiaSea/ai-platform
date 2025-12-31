from pydantic import BaseModel
from fastapi import HTTPException
import requests

def call_ollama_format(
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
        resp = requests.post(
            "http://localhost:8001/api/chat",
            json=payload,
            timeout=100,
        )
        resp.raise_for_status() 
    except requests.RequestException:
        raise HTTPException(502, "推理超时或 Ollama 服务异常")

    data = resp.json()
    content = data.get("message", {}).get("content", "")

    # ⭐ 核心防护：不要把空字符串交给 pydantic
    if not content or not content.strip():
        return schema.model_validate({})

    return schema.model_validate_json(content)


def call_ollama(
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
        resp = requests.post(
            "http://localhost:8001/api/chat",
            json=payload,
            timeout=200,
        )
        resp.raise_for_status() 
    except requests.RequestException:
        raise HTTPException(502, "推理超时或 Ollama 服务异常")
    return resp.json()["message"]["content"]