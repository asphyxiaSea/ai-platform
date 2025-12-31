from typing import List
from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
from util.call_ollama import call_ollama_format

from util.marker_pdf import MarkerPDF
from io import BytesIO

def chat_texts_pdfs_services(
    taskconfig:TaskConfig,
    pdf_bytes_list: List[bytes]
) -> BaseModel:

    texts = []
    if taskconfig.marker_pdf is None:
        taskconfig.marker_pdf = MarkerPDF()
    for idx, pdf_bytes in enumerate(pdf_bytes_list):
        text = taskconfig.marker_pdf.extract_text(BytesIO(pdf_bytes))
        texts.append(f"[PDF {idx+1}]\n{text}")

    merged_text = "\n\n".join(texts)
    return _call_ollama(
        taskconfig=taskconfig,
        texts=merged_text
    )


def _call_ollama(
    taskconfig: TaskConfig,
    texts: str
) -> BaseModel :

    schema = taskconfig.schema

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
    )

    task_description = (schema.__doc__ or "").strip()

    full_prompt = f"""
[任务说明]
{task_description}
[所需字段及说明]
{field_prompts}
[文档内容]
{texts}
"""

    messages = [
        {"role": "user", "content": full_prompt}
    ]

    return call_ollama_format(
        model=taskconfig.model,
        schema=schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )