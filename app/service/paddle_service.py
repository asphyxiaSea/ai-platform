from pydantic import BaseModel
from app.domain.task_config_factory import TaskConfig
from app.domain.file_item import FileItem
from app.infra.paddle_client import extract_file
from app.infra.llm_client import structured_output
from app.domain.postprocess import text_postprocess


async def paddle_services(
    taskconfig: TaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    results: list[BaseModel] = []
    for file_item in file_items:
        # 1. paddle → text
        text = await extract_file(file_item=file_item)
        final_text = text_postprocess(
            text,
            target_sections=taskconfig.postprocess.get("target_sections", [])
            if taskconfig.postprocess
            else None,
        )
        print(final_text)

        # 3. text → LLM
        result = await _call_ollama(taskconfig=taskconfig, text=final_text)
        results.append(result)

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
    task_description = (taskconfig.system_prompt).strip()

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
