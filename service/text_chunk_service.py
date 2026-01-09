import re
from io import BytesIO
from typing import List, Dict
from pydantic import BaseModel
from domain.task_config import TaskConfig
from util.ollama import ollama_format_output,ollama_output

PAGE_RE = re.compile(r"^\{(\d+)\}-+$")

# def chat_text_pdfs_service(
#     taskconfig: TaskConfig,
#     pdf_bytes_list: list[bytes],
# ) -> BaseModel:
#     """
#     多 PDF → 各自分页 → 3 页 Map → 全局 Merge → Reduce
#     """

#     if not pdf_bytes_list:
#         return taskconfig.schema.model_validate({})


#     all_page_results: list[str] = []

#     # 2️⃣ 每个 PDF 独立 Map
#     for pdf_idx, pdf_bytes in enumerate(pdf_bytes_list, start=1):
#         raw_text = extract_pdf(pdf=BytesIO(pdf_bytes),marker=taskconfig.marker)

#         page_results = map_extract_pages(
#             taskconfig=taskconfig,
#             raw_text=raw_text,
#             pages_per_chunk=3,
#         )

#         if not page_results:
#             continue

#         # 给每个 PDF 加一个边界标签（非常重要）
#         for r in page_results:
#             all_page_results.append(
#                 f"[PDF {pdf_idx}]\n{r}"
#             )

#     if not all_page_results:
#         return taskconfig.schema.model_validate({})

#     # 3️⃣ 全局 Merge
#     merged_text = merge_page_results(all_page_results)
#     print(merged_text)

#     # 4️⃣ Reduce（一次结构化）
#     return _call_ollama(
#         taskconfig=taskconfig,
#         text=merged_text,
#     )



def split_marker_pdf_pages(text: str) -> List[Dict]:
    pages = []
    current_page = None
    buffer = []

    for line in text.splitlines():
        m = PAGE_RE.match(line.strip())
        if m:
            if current_page is not None:
                pages.append({
                    "page": current_page + 1,  # 转成 1-based
                    "text": "\n".join(buffer).strip()
                })
                buffer = []
            current_page = int(m.group(1))
        else:
            buffer.append(line)

    if current_page is not None:
        pages.append({
            "page": current_page + 1,
            "text": "\n".join(buffer).strip()
        })

    return pages

def chunk_pages(pages: list[dict], chunk_size: int) -> List[List[dict]]:
    """
    把 pages 按 chunk_size 分组
    """
    return [
        pages[i:i + chunk_size]
        for i in range(0, len(pages), chunk_size)
    ]

def map_extract_pages(
    taskconfig: TaskConfig,
    raw_text: str,
    pages_per_chunk: int = 3,
) -> list[str]:
    """
    每 pages_per_chunk 页做一次 Map 抽取
    """
    pages = split_marker_pdf_pages(raw_text)
    page_chunks = chunk_pages(pages, pages_per_chunk)

    chunk_results: list[str] = []

    for chunk in page_chunks:
        # 拼 chunk 文本（保留页码）
        chunk_text_parts = []

        for page in chunk:
            if not page["text"]:
                continue

            chunk_text_parts.append(
f"""
[第 {page['page']} 页]
{page['text']}
"""
            )

        if not chunk_text_parts:
            continue

        chunk_text = "\n".join(chunk_text_parts)

        result = _call_ollama_chunk(
            taskconfig=taskconfig,
            texts=chunk_text,
        )

        if result and result.strip():
            pages_range = f"{chunk[0]['page']}-{chunk[-1]['page']}"
            chunk_results.append(
                f"[第 {pages_range} 页]\n{result.strip()}"
            )

    return chunk_results


def merge_page_results(page_results: list[str]) -> str:
    """
    把 Map 阶段结果拼成一个干净文本
    """
    return "\n\n".join(page_results)


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



def _call_ollama_chunk(
    taskconfig: TaskConfig,
    texts: str
) -> str:

    field_prompts = "; ".join(
        f"{name}: {field.description}"
        for name, field in taskconfig.schema.model_fields.items()
    )

    system_prompt = f"""
你是一个中文文档关键信息抽取助手。

【抽取规则】
1. 仅允许抽取【字段范围】内的信息
2. 仅当文档中明确出现时才抽取
3. 不要总结、不要推理、不要补全
4. 不要引入字段范围之外的信息

【字段范围】
{field_prompts}

【输出要求】
- 输出为一段简洁文本
- 内容必须可直接对应到上述字段的原文信息片段
- 不要输出解释、说明或无关内容
""".strip()

    user_prompt = f"""
[文档内容]
{texts}
""".strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return ollama_output(
        model=taskconfig.model,
        messages=messages,
        temperature=taskconfig.temperature,
    )