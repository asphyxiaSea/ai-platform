from typing import List,Optional,Dict, Any,Type
from fastapi import HTTPException
import requests
from util.pdf_utils import pdf_bytes_to_base64_images,image_bytes_to_base64
from pydantic import BaseModel
from schemas.registry import SCHEMA_REGISTRY



def chat_text_only(model: str, prompt: str,schema_name: str) -> BaseModel:
    return _call_ollama(
        model=model,
        prompt=prompt,
        schema_name=schema_name
    )

def chat_with_images(model: str,prompt: str,schema_name: str,images: List[bytes]) -> BaseModel:
    if not images:
        raise HTTPException(400, "images is required")

    images_bytes = [
        image_bytes_to_base64(b) for b in images
    ]

    return _call_ollama(
        model=model,
        prompt=prompt,
        schema_name=schema_name,
        images_bytes=images_bytes
    )

def chat_with_pdf(model: str, prompt: str, schema_name: str,pdf_bytes: bytes) -> BaseModel:
    images_bytes = pdf_bytes_to_base64_images(pdf_bytes)

    if not images_bytes:
        raise HTTPException(400, "PDF contains no pages")

    return _call_ollama(
        model=model,
        prompt=prompt,
        schema_name=schema_name,
        images_bytes=images_bytes
    )

def _call_ollama(
    model: str,
    prompt: str,
    schema_name: str,
    images_bytes: Optional[List[str]] = None
) -> BaseModel:
    """
    Ollama 统一调用入口
    """
    
    message: Dict[str, Any] = {
        "role": "user",
        "content": prompt,
    }

    # 获取类
    Schema = SCHEMA_REGISTRY.get(schema_name)
    if not Schema:
        raise HTTPException(400, f"Unknown schema: {schema_name}")

    if images_bytes:
        message["images"] = images_bytes

    payload = {
        "model": model,
        "messages": [message],
        "stream": False,
        # ollama强束缚，对提示词有要求，不然会卡死
        # 为什么 OpenAI 的 Structured Outputs 不会这样？
            # 这是非常关键的区别 👇
            # OpenAI Structured Outputs（Responses API）
            # 不是靠模型“硬想JSON”
            # 是先生成结构化token
            # 再在系统层保证合法性
        "format":Schema.model_json_schema()
    }

    try:
        resp = requests.post(
            "http://localhost:8001/api/chat",
            json=payload,
            timeout=100,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(502, f"推理超时，更换提示词试试")
    print(Schema.model_validate_json(resp.json()["message"]["content"]))
    return Schema.model_validate_json(resp.json()["message"]["content"])
