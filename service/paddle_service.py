from typing import List
from pydantic import BaseModel
from domain.task_config_factory import TaskConfig
from domain.file_item import FileItem
from domain.paddle import extract_file
from util.ollama import ollama_format_output

def paddle_services(
    taskconfig: TaskConfig,
    file_items: list[FileItem],
) -> BaseModel:
    results: List[BaseModel] = []
    for file_item in file_items:
        # 1. marker → text
        text = extract_file(file_item=file_item)
        print(text)
        # 3. text → LLM
        result = _call_ollama(taskconfig=taskconfig, text=text)
        results.append(result)

    # 当前逻辑：只取第一个（如果这是你 schema 设计决定的）

    return results[0]


def _call_ollama(
    taskconfig: TaskConfig,
    text: str
) -> BaseModel:

    # 1️⃣ 字段说明
    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    # 2️⃣ 任务说明（schema docstring）
    task_description = (taskconfig.system_prompt).strip()

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

    return ollama_format_output(
        model=taskconfig.model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )
