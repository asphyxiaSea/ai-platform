from typing import List,Optional,Dict, Any
from fastapi import HTTPException
from util.pdf_utils import pdf_bytes_to_base64_images,image_bytes_to_base64
from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
import requests

def chat_multimodal_images_services(taskconfig:TaskConfig,image_bytes_list: List[bytes]) -> BaseModel:
    if not image_bytes_list:
        raise HTTPException(400, "image_bytes_list is required")

    images_base64_list = [
        image_bytes_to_base64(b) for b in image_bytes_list
    ]
    return _call_multimodal_ollama(
        taskconfig=taskconfig,
        images_base64_list=images_base64_list
    )


def chat_multimodal_pdfs_services(
    taskconfig: TaskConfig,
    pdf_bytes_list: List[bytes]
) -> BaseModel:

    images_base64_list = []

    for idx, pdf_bytes in enumerate(pdf_bytes_list):
        images_bytes = pdf_bytes_to_base64_images(pdf_bytes)

        # 合并所有 PDF 的图片
        images_base64_list.extend(images_bytes)

    return _call_multimodal_ollama(
        taskconfig=taskconfig,
        images_base64_list=images_base64_list
    )

# 多模态调用ollama
def _call_multimodal_ollama(
    taskconfig: TaskConfig,
    images_base64_list: Optional[List[str]] = None
) -> BaseModel:
    schema = taskconfig.schema
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

    if images_base64_list:
        message["images"] = images_base64_list

    payload = {
        "model": taskconfig.vl_model,
        "messages": [message],
        "stream": False,
        "temperature":taskconfig.temperature,
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
