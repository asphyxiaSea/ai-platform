from typing import Any, Iterable, Protocol
from pydantic import BaseModel
from app.domain.templates.files_parse.config import FilesTaskConfig
from app.domain.capabilities.llm.llm_config import DEFAULT_SYSTEM_PROMPT


class HasLLMConfig(Protocol):
    schema: type[BaseModel]
    system_prompt: str


def build_ollama_messages(
    *,
    taskconfig: HasLLMConfig,
    text: str,
    image_base64_list: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    task_description = (taskconfig.system_prompt or DEFAULT_SYSTEM_PROMPT).strip()

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
