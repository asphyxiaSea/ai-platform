from typing import Any
from app.domain.task_config_factory import FilesTaskConfig, LLMTaskConfig


def build_ollama_messages(
    *,
    taskconfig: FilesTaskConfig,
    text: str,
) -> list[dict[str, str]]:
    # 1) 字段说明
    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    # 2) 任务说明（schema docstring）
    task_description = taskconfig.system_prompt.strip()

    # 3) system prompt：规则 + 约束
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

    return messages


def build_multimodal_ollama_messages(
    *,
    taskconfig: LLMTaskConfig,
    image_base64_list: list[str],
) -> list[dict[str, Any]]:
    schema = taskconfig.schema

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
    )

    task_description = (schema.__doc__ or "").strip()

    # 3) system prompt：规则 + 约束
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
            "images": image_base64_list,
        },
    ]

    return messages


def build_openai_messages(
    *,
    taskconfig: FilesTaskConfig,
    text: str,
) -> list[dict[str, str]]:
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

    return messages
