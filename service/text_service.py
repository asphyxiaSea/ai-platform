from typing import List
from fastapi import HTTPException
import requests
from pydantic import BaseModel
from schemas.registry import SCHEMA_REGISTRY

from marker.output import text_from_rendered
from util.mark_pdf import CONVERTER
from io import BytesIO

def chat_texts_pdfs_services(
    schema_name: str,
    pdf_bytes_list: List[bytes]
) -> BaseModel:

    texts = []

    for idx, pdf_bytes in enumerate(pdf_bytes_list):
        rendered = CONVERTER(BytesIO(pdf_bytes))
        full_text, _, _ = text_from_rendered(rendered)

        texts.append(f"【PDF {idx+1}】\n{full_text}")

    merged_text = "\n\n".join(texts)
    
    return _call_ollama(
        schema_name=schema_name,
        texts=merged_text
    )


def _call_ollama(
    schema_name: str,
    texts: str
) -> BaseModel:

    schema = SCHEMA_REGISTRY[schema_name].schema
    if not schema:
        raise HTTPException(400, f"Unknown schema: {schema_name}")

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in schema.model_fields.items()
)
    task_description = (schema.__doc__ or "").strip()

    full_prompt = f"""
[任务说明]
{task_description}
[字段提示]
{field_prompts}
[文档内容]
{texts}
"""
    
    messages = [{"role": "user","content": full_prompt}]

    payload = {
        "model": SCHEMA_REGISTRY[schema_name].model,
        "messages": messages,
        "stream": False,
        "temperature":SCHEMA_REGISTRY[schema_name].temperature,
        # ollama强束缚,保证输出合法性
        "format": schema.model_json_schema()
    }

    try:
        resp = requests.post(
            "http://localhost:8001/api/chat",
            json=payload,
            timeout=100,
        )
        resp.raise_for_status()
    except requests.RequestException:
        raise HTTPException(502, "推理超时或 Ollama 服务异常")

    return schema.model_validate_json(resp.json()["message"]["content"])