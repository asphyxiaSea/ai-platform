from typing import List
from pydantic import BaseModel
from app.domain.task_config_factory import TaskConfig
from app.infra.llm_client import structured_output
from app.infra.marker_client import extract_file
from app.domain.file_item import FileItem


async def marker_services(
    taskconfig: TaskConfig,
    file_items: list[FileItem],
) -> dict[str, List[BaseModel]]:

    results: List[BaseModel] = []

    for file_item in file_items:
        # 1. marker → text
        text = await extract_file(file_item=file_item, marker=taskconfig.marker)

        # 3. text → LLM
        result = await _call_ollama(taskconfig=taskconfig, text=text)
        results.append(result)

    # 当前逻辑：只取第一个（如果这是你 schema 设计决定的）
    return {
        "results": results  # 这里定义的键名要与输出变量名一致
    }


async def _call_ollama(
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
    task_description = (taskconfig.schema.__doc__ or "").strip()

    # 3️⃣ system prompt：规则 + 约束
    system_prompt = f"""
【任务说明】
{task_description}

【字段定义】
{field_prompts}
""".strip()

    user_prompt = f"""
【文档内容】
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


async def _call_openai(
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
