from pydantic import BaseModel
from schemas.taskconfig import TaskConfig
from util.ollama import ollama_format_output,ollama_output
import re
from typing import List, Dict
from util.marker_pdf import MarkerPDF
from io import BytesIO

PAGE_RE = re.compile(r"^\{(\d+)\}-+$")

def chat_text_pdfs_service(
    taskconfig: TaskConfig,
    pdf_bytes_list: list[bytes],
) -> BaseModel:
    """
    多 PDF → 各自分页 → 3 页 Map → 全局 Merge → Reduce
    """

    if not pdf_bytes_list:
        return taskconfig.schema.model_validate({})

    # 1️⃣ marker-pdf 初始化
    if taskconfig.marker_pdf is None:
        taskconfig.marker_pdf = MarkerPDF()

    all_page_results: list[str] = []

    # 2️⃣ 每个 PDF 独立 Map
    for pdf_idx, pdf_bytes in enumerate(pdf_bytes_list, start=1):

        raw_text = taskconfig.marker_pdf.extract_text(
            BytesIO(pdf_bytes)
        )

        page_results = map_extract_pages(
            taskconfig=taskconfig,
            raw_text=raw_text,
            pages_per_chunk=3,
        )

        if not page_results:
            continue

        # 给每个 PDF 加一个边界标签（非常重要）
        for r in page_results:
            all_page_results.append(
                f"[PDF {pdf_idx}]\n{r}"
            )

    if not all_page_results:
        return taskconfig.schema.model_validate({})

    # 3️⃣ 全局 Merge
    merged_text = merge_page_results(all_page_results)
    print(merged_text)

    # 4️⃣ Reduce（一次结构化）
    return _call_ollama_format(
        taskconfig=taskconfig,
        texts=merged_text,
    )



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

        result = _call_ollama(
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


def _call_ollama_format(
    taskconfig: TaskConfig,
    texts: str
) -> BaseModel:

    schema = taskconfig.schema

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

    messages = [
        {"role": "user", "content": full_prompt}
    ]

    return ollama_format_output(
        model=taskconfig.model,
        schema=schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )

def _call_ollama(
    taskconfig: TaskConfig,
    texts: str
) -> str:

    schema = taskconfig.schema

    field_prompts = ";".join(
        f"{name}: {field.description}"
        for name, field in schema.model_fields.items()
    )

    full_prompt = f"""
从下列中文文档中抽取关键信息要点。

规则：
1. 仅允许提取【以下字段范围】内的信息
2. 仅当文档中明确出现时才提取
3. 不要总结、不要推理、不要补全
4. 不要引入字段范围之外的信息

字段范围：
{field_prompts}

输出：
用一段简洁文本，只包含可直接对应到上述字段的原文信息片段。
[文档内容]
{texts}
"""

    messages = [
        {"role": "user", "content": full_prompt}
    ]

    return ollama_output(
        model=taskconfig.model,
        messages=messages,
        temperature=taskconfig.temperature,
    )