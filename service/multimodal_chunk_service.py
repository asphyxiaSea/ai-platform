from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
from util.ollama import ollama_format_output,ollama_output
from util.pdf_utils import pdf_bytes_to_base64_images

def chat_pdfs_images_services(
    taskconfig: TaskConfig,
    pdf_bytes_list: List[bytes]
) -> List[BaseModel]:

    if not pdf_bytes_list:
        raise HTTPException(400, "pdf_bytes_list is required")

    results: List[BaseModel] = []

    for pdf_idx, pdf_bytes in enumerate(pdf_bytes_list, start=1):

        images_base64 = pdf_bytes_to_base64_images(pdf_bytes)

        page_chunks: list[str] = []

        # ⭐ 每 3 页一组
        for start in range(0, len(images_base64), 3):
            image_group = images_base64[start:start + 3]
            page_range = f"{start + 1}-{min(start + 3, len(images_base64))}"

            chunk_text = _call_multimodal_chunk_ollama(
                taskconfig=taskconfig,
                images_base64=image_group,  # 👈 这里是 list[str]
            )

            print(f"[PDF {pdf_idx}] pages {page_range}")
            print(chunk_text)

            if chunk_text and chunk_text.strip():
                page_chunks.append(
                    f"【第{page_range}页】\n{chunk_text}"
                )

        # 🔑 一个 PDF 的“可用文本”
        merged_text = "\n\n".join(page_chunks)

        # 👉 用纯文本模型做最终结构化
        final_result = _call_ollama(
            taskconfig=taskconfig,
            text=merged_text,
        )

        results.append(final_result)

    return results
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
用自己的语言，描述这几页写了什么，不要漏掉关键信息。
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



def _call_multimodal_chunk_ollama(
    taskconfig: TaskConfig,
    images_base64: list[str],
) -> str:

    field_prompts = "\n".join(
        f"- {name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
        if field.description
    )

    system_prompt = f"""
你是一个中文文档信息抽取助手。

任务：
- 从图片中寻找【与字段相关的原文信息片段线索】。

规则：
1. 仅抽取字段范围内的信息
2. 仅当图片中明确出现时才输出
3. 不要总结、不要推理、不要补全、不要输出字段名。
4. 字段范围内的信息用正常人的语言方式描述。

字段范围：
{field_prompts}

""".strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"请根据图片内容进行信息抽取。",
            "images": images_base64
        },
    ]

    return ollama_output(
        model=taskconfig.vl_model,
        messages=messages,
        temperature=taskconfig.temperature,
    )