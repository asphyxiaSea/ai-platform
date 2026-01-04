from typing import List,Optional, Any
from fastapi import HTTPException
from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
from util.ollama import ollama_format_output
from util.openai import openai_structure_output
from util.pdf_utils import pdf_bytes_to_base64_images,image_bytes_to_base64

def chat_multimodal_images_services(
    taskconfig: TaskConfig,
    image_bytes_list: List[bytes]
) -> List[BaseModel]:

    if not image_bytes_list:
        raise HTTPException(400, "image_bytes_list is required")

    results: List[BaseModel] = []

    for idx, image_bytes in enumerate(image_bytes_list, start=1):
        image_base64 = image_bytes_to_base64(image_bytes)

        result = _call_multimodal_ollama(
            taskconfig=taskconfig,
            image_base64=image_base64
        )

        results.append(result)

    return results

def chat_multimodal_pdfs_services(
    taskconfig: TaskConfig,
    pdf_bytes_list: List[bytes]
) -> List[BaseModel]:

    if not pdf_bytes_list:
        raise HTTPException(400, "pdf_bytes_list is required")

    results: List[BaseModel] = []

    for idx, pdf_bytes in enumerate(pdf_bytes_list, start=1):
        images_base64 = pdf_bytes_to_base64_images(pdf_bytes)
        for image_base64 in images_base64:
            # 每个 PDF 单独调用一次
            result = _call_multimodal_ollama(
                taskconfig=taskconfig,
                image_base64=image_base64
            )

        results.append(result)

    return results

# 多模态调用ollama
def _call_multimodal_ollama(
    taskconfig: TaskConfig,
    image_base64: Optional[str] = None
) -> BaseModel:

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    task_description = (taskconfig.schema.__doc__ or "").strip()

    system_prompt = f"""
【任务说明】
{task_description}

【字段定义】
{field_prompts}
""".strip()

    user_message: dict[str, Any] = {
        "role": "user",
        "content": "请根据图片内容进行信息抽取。"
    }

    if image_base64:
        user_message["images"] = [image_base64]

    messages = [
        {"role": "system", "content": system_prompt},
        user_message,
    ]

    return ollama_format_output(
        model=taskconfig.vl_model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )

def _call_multimodal_openai(
    taskconfig: TaskConfig,
    image_base64: Optional[str] = None
) -> BaseModel:

    messages = [
        {
            "role": "system", 
            "content": (taskconfig.schema.__doc__ or "").strip()
        },
        {
            "role": "user", 
            "content":
        [
            {
                "type": "text", 
                "text": "请从以下图片中提取信息："
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            }
        ]},
    ]

    return openai_structure_output(
        model=taskconfig.model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )
