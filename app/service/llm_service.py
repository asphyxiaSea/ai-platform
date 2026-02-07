from pydantic import BaseModel
from typing import Any
from app.domain.task_config_factory import TaskConfig
from app.domain.file_item import FileItem
from app.infra.llm_client import structured_output
from app.util.pdf_utils import image_bytes_to_base64, pdf_bytes_to_base64_images
from app.domain.file_item import FileItem

async def multimodal_llm_services(
    taskconfig: TaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    results: list[BaseModel] = []
    for file_item in file_items:

        result = await call_multimodal_ollama(taskconfig=taskconfig, image_base64=file_item.data)
        results.append(result)

    return {
        "results": results  # 这里定义的键名要与输出变量名一致
    }



async def call_ollama(
    *,
    taskconfig: TaskConfig,
    text: str,
) -> BaseModel:
    # 1️⃣ 字段说明
    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    # 2️⃣ 任务说明（schema docstring）
    task_description = taskconfig.system_prompt.strip()

    # 3️⃣ system prompt：规则 + 约束
    system_prompt = f"""
【任务说明】
{task_description}

【字段定义】
{field_prompts}
""".strip()

    user_prompt = f"""
{text}
""".strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return await structured_output(
        model=taskconfig.model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )

# 多模态调用ollama
async def call_multimodal_ollama(
    taskconfig: TaskConfig,
    image_base64: bytes,
) -> BaseModel:

    schema = taskconfig.schema

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
    )

    task_description = (schema.__doc__ or "").strip()

    # 3️⃣ system prompt：规则 + 约束
    system_prompt = f"""
【任务说明】
{task_description}

【字段定义】
{field_prompts}
""".strip()


    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": "请根据图片完成上述任务。",
            "images" : image_base64
        }
    ]

    return await structured_output(
        model=taskconfig.vl_model,
        schema=schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )

async def call_openai(
    *,
    taskconfig: TaskConfig,
    text: str,
) -> BaseModel:
    messages = [
        {
            "role": "system",
            "content": (taskconfig.schema.__doc__ or "").strip(),
        },
        {
            "role": "user",
            "content": f"请从以下文本中提取信息：\n\n{text}",
        },
    ]

    return await structured_output(
        model=taskconfig.model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
        backend="openai",
    )
