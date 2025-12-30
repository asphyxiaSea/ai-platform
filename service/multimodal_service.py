from typing import List,Optional, Any
from fastapi import HTTPException
from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
from util.call_ollama import call_ollama_format
from util.pdf_utils import pdf_bytes_to_base64_images,image_bytes_to_base64

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
    images_base64_list: Optional[list[str]] = None
) -> BaseModel:

    schema = taskconfig.schema

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
    )

    task_description = (schema.__doc__ or "").strip()

    message: dict[str, Any] = {
        "role": "user",
        "content": f"""
[任务说明]
{task_description}
[字段提示]
{field_prompts}
""",
    }

    if images_base64_list:
        message["images"] = images_base64_list

    return call_ollama_format(
        model=taskconfig.vl_model,
        schema=schema,
        messages=[message],
        temperature=taskconfig.temperature,
    )
