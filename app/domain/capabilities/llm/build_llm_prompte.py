from typing import Any, Iterable
from pydantic import BaseModel

DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
""".strip()


def build_ollama_messages(
    *,
    schema: type[BaseModel],
    system_prompt: str | None,
    text: str,
    image_base64_list: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
        if field.description
    )

    task_description = (system_prompt or DEFAULT_SYSTEM_PROMPT).strip()

    system_prompt = f"""
【任务说明】
{task_description}

【字段定义】
{field_prompts}
""".strip()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text.strip()},
    ]

    if image_base64_list:
        messages[-1]["images"] = list(image_base64_list)

    return messages


def build_openai_messages(
    *,
    schema: type[BaseModel],
    system_prompt: str | None,
    text: str,
) -> list[dict[str, str]]:
    resolved_system_prompt = (
        system_prompt or schema.__doc__ or DEFAULT_SYSTEM_PROMPT
    ).strip()
    messages = [
        {
            "role": "system",
            "content": resolved_system_prompt,
        },
        {
            "role": "user",
            "content": f"请从以下文本中提取信息：\n\n{text}",
        },
    ]

    return messages
