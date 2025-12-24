from typing import List,Optional,Dict, Any
from fastapi import HTTPException
from util.pdf_utils import pdf_bytes_to_base64_images,image_bytes_to_base64
from pydantic import BaseModel
from schemas.registry import SCHEMA_REGISTRY
import requests

def chat_multimodal_images_services(schema_name: str,images: List[bytes]) -> BaseModel:
    if not images:
        raise HTTPException(400, "images is required")

    images_bytes = [
        image_bytes_to_base64(b) for b in images
    ]

    return _call_multimodal_ollama(
        schema_name=schema_name,
        images_bytes=images_bytes
    )


def chat_multimodal_pdfs_services(
    schema_name: str,
    pdf_bytes_list: List[bytes]
) -> BaseModel:

    all_images_bytes = []

    for idx, pdf_bytes in enumerate(pdf_bytes_list):
        images_bytes = pdf_bytes_to_base64_images(pdf_bytes)

        # 合并所有 PDF 的图片
        all_images_bytes.extend(images_bytes)

    return _call_multimodal_ollama(
        schema_name=schema_name,
        images_bytes=all_images_bytes
    )

# 多模态调用ollama
def _call_multimodal_ollama(
    schema_name: str,
    images_bytes: Optional[List[str]] = None
) -> BaseModel:

    # 获取类
    schema = SCHEMA_REGISTRY[schema_name].schema
    if not schema:
        raise HTTPException(400, f"Unknown schema: {schema_name}")

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
    )

    task_description = (schema.__doc__ or "").strip()

    full_prompt = f"""
[任务说明]
{task_description}
[字段提示]
{field_prompts}
"""
    
    message: Dict[str, Any] = {
        "role": "user",
        "content": full_prompt,
    }

    if images_bytes:
        message["images"] = images_bytes

    payload = {
        "model": SCHEMA_REGISTRY[schema_name].model,
        "messages": [message],
        "stream": False,
        "temperature":SCHEMA_REGISTRY[schema_name].temperature,
        # ollama强束缚,保证输出合法性
        "format":schema.model_json_schema()
    }

    try:
        resp = requests.post(
            "http://localhost:8001/api/chat",
            json=payload,
            timeout=100,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(502, "推理超时或 Ollama 服务异常")
    return schema.model_validate_json(resp.json()["message"]["content"])
