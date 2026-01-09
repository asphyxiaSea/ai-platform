from typing import List
from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
from util.ollama import ollama_format_output
from util.openai import openai_structure_output
from util.marker import extract_pdf,extract_file
from io import BytesIO

def chat_texts_pdfs_services(
    taskconfig:TaskConfig,
    pdf_bytes_list: List[bytes]
) -> BaseModel:
    results: List[BaseModel] = []
    for idx, pdf_bytes in enumerate(pdf_bytes_list):
        text = extract_pdf(pdf=BytesIO(pdf_bytes),marker=taskconfig.marker)
        # print(text)
        results.append(_call_ollama(
            taskconfig=taskconfig,
            text=text
        ))
    return results[0]


def chat_texts_pdfs_services_list(
    taskconfig:TaskConfig,
    pdf_bytes_list: List[bytes]
) -> List[BaseModel]:
    results: List[BaseModel] = []
    for idx, pdf_bytes in enumerate(pdf_bytes_list):
        text = extract_pdf(pdf=BytesIO(pdf_bytes),marker=taskconfig.marker)
        results.append(_call_ollama(
            taskconfig=taskconfig,
            text=text
        ))
    return results

def chat_texts_images_services(
    taskconfig:TaskConfig,
    image_bytes_list: List[bytes]
) -> BaseModel:
    results: List[BaseModel] = []
    for idx, image_bytes in enumerate(image_bytes_list):
        text = extract_file(file=BytesIO(image_bytes),marker=taskconfig.marker)
        results.append(_call_ollama(
            taskconfig=taskconfig,
            text=text
        ))
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

    return ollama_format_output(
        model=taskconfig.model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )


def _call_openai(
    taskconfig: TaskConfig,
    text: str
) -> BaseModel:

    messages = [
        {
            "role": "system", 
            "content": (taskconfig.schema.__doc__ or "").strip()
        },
        {
            "role": "user", 
            "content": f"请从以下文本中提取信息：\n\n{text}"
        },
    ]

    return openai_structure_output(
        model=taskconfig.model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )
