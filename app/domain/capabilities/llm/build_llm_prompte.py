from typing import Any, Iterable
from app.domain.templates.files_parse.config import FilesTaskConfig
from app.domain.templates.llm_chat.config import LLMTaskConfig


def build_ollama_messages(
    *,
    taskconfig: FilesTaskConfig | LLMTaskConfig,
    prompt: str,
    image_base64_list: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    task_description = (getattr(taskconfig, "system_prompt", "") or "").strip()

    system_prompt = f"""
【任务说明】
{task_description}

【字段定义】
{field_prompts}
""".strip()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt.strip()},
    ]

    if image_base64_list:
        messages[-1]["images"] = list(image_base64_list)

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
