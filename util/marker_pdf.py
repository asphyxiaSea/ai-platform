import io
import json
import requests
from typing import Any, Optional, Union

DEFAULT_PROCESSORS: dict[str, str] = {
    # ===== 基础顺序 / 结构 =====
    "order": "marker.processors.order.OrderProcessor",
    "block_relabel": "marker.processors.block_relabel.BlockRelabelProcessor",
    "line_merge": "marker.processors.line_merge.LineMergeProcessor",

    # ===== 语义块 =====
    "blockquote": "marker.processors.blockquote.BlockquoteProcessor",
    "code": "marker.processors.code.CodeProcessor",
    "equation": "marker.processors.equation.EquationProcessor",
    "footnote": "marker.processors.footnote.FootnoteProcessor",
    "list": "marker.processors.list.ListProcessor",
    "text": "marker.processors.text.TextProcessor",

    # ===== 文档结构 =====
    "toc": "marker.processors.document_toc.DocumentTOCProcessor",
    "page_header": "marker.processors.page_header.PageHeaderProcessor",
    "section_header": "marker.processors.sectionheader.SectionHeaderProcessor",
    "line_numbers": "marker.processors.line_numbers.LineNumbersProcessor",
    "reference": "marker.processors.reference.ReferenceProcessor",
    "blank_page": "marker.processors.blank_page.BlankPageProcessor",

    # ===== 表格 / 表单 =====
    "table": "marker.processors.table.TableProcessor",
    "llm_table": "marker.processors.llm.llm_table.LLMTableProcessor",
    "llm_table_merge": "marker.processors.llm.llm_table_merge.LLMTableMergeProcessor",
    "llm_form": "marker.processors.llm.llm_form.LLMFormProcessor",

    # ===== LLM 增强区域 =====
    "llm_complex_region": "marker.processors.llm.llm_complex.LLMComplexRegionProcessor",
    "llm_image_description": "marker.processors.llm.llm_image_description.LLMImageDescriptionProcessor",
    "llm_equation": "marker.processors.llm.llm_equation.LLMEquationProcessor",
    "llm_handwriting": "marker.processors.llm.llm_handwriting.LLMHandwritingProcessor",
    "llm_math_block": "marker.processors.llm.llm_mathblock.LLMMathBlockProcessor",
    "llm_section_header": "marker.processors.llm.llm_sectionheader.LLMSectionHeaderProcessor",
    "llm_page_correction": "marker.processors.llm.llm_page_correction.LLMPageCorrectionProcessor",

    # ===== 调试 =====
    "debug": "marker.processors.debug.DebugProcessor",

    # ===== 忽略明确噪声文本 =====
    "ignoretext": "marker.processors.ignoretext.IgnoreTextProcessor"
}

DEFAULT_PROCESSORS_NAME = [
        # 1️⃣ 顺序 & 稳定（必须）
        "order",
        "block_relabel",
        "line_merge",

        # 2️⃣ 常见结构
        "list",
        "page_header",
        "section_header",
        "reference",
        "toc",

        # 4️⃣ 输出
        "text",
        "blank_page",
    ]

class MarkerPDF:
    def __init__(
        self,
        page_range: list[int] | None = None,
        extract_images: bool = False,
        output_format: str = "markdown",
        filter_noisy: bool = False,
        remove_processors: list[str] | None = None,
        append_processors: list[str] | None = None,
    ):
        self.page_range = page_range
        self.extract_images = extract_images
        self.output_format = output_format
        self.filter_noisy = filter_noisy
        self.remove_processors = remove_processors
        self.append_processors = append_processors

    def to_config(self) -> dict[str, Any]:
        cfg = {
            "output_format": self.output_format,
            "extract_images": self.extract_images,
        }
        if self.page_range:
            cfg["page_range"] = self.page_range
        return cfg

    def to_processor_list(self) -> list[str] | None:
        # ---- 1️⃣ remove 校验 ----
        if self.remove_processors:
            invalid = set(self.remove_processors) - set(DEFAULT_PROCESSORS)
            if invalid:
                raise ValueError(
                    f"Unknown processors in remove_processors: {invalid}"
                )

        # ---- 2️⃣ append 校验 ----
        if self.append_processors:
            invalid = set(self.append_processors) - set(self.append_processors)
            if invalid:
                raise ValueError(
                    f"Unknown processors in append_processors: {invalid}"
                )

        # ---- 3️⃣ 构建 pipeline（先 remove）----
        ignored = set(self.remove_processors or [])
        processor_names = [
            name for name in DEFAULT_PROCESSORS_NAME
            if name not in ignored
        ]

        # ---- 4️⃣ append ----
        if self.append_processors:
            for name in self.append_processors:
                if name not in processor_names:
                    processor_names.append(name)

        # ---- 5️⃣ 映射为 processor 类 ----
        processor_list = [
            DEFAULT_PROCESSORS[name]
            for name in processor_names
        ]
        print(processor_list)
        return processor_list

        # processor_names = [
        #     p for p in DEFAULT_PROCESSORS_NAME
        #     if p not in (self.remove_processors or [])
        # ]

        # if self.append_processors:
        #     for p in self.append_processors:
        #         if p not in processor_names:
        #             processor_names.append(p)

        # return [
        #     DEFAULT_PROCESSORS[name]
        #     for name in processor_names
        # ]


def extract_pdf(
    *,
    pdf: Union[str, io.BytesIO],
    markerpdf: MarkerPDF | None = None,
) -> str:
    url = "http://localhost:8004/marker-pdf/extract"

    if isinstance(pdf, str):
        with open(pdf, "rb") as f:
            pdf_io = io.BytesIO(f.read())
        filename = pdf.split("/")[-1]
    else:
        pdf_io = pdf
        filename = "input.pdf"

    data = {}

    if markerpdf is not None:
        data["config"] = json.dumps(markerpdf.to_config(), ensure_ascii=False)
        processor_list = markerpdf.to_processor_list()
        if processor_list is not None:
            data["processor_list"] = json.dumps(processor_list, ensure_ascii=False)

    resp = requests.post(
        url,
        files={"file": (filename, pdf_io, "application/pdf")},
        data=data,
        timeout=200,
    )

    resp.raise_for_status()
    if markerpdf is not None and markerpdf.filter_noisy:
        return filter_noisy(resp.json()["text"])
    else:
        return resp.json()["text"]


import re

def filter_noisy(full_text: str) -> str:
    lines = full_text.splitlines()

    # 按长度过滤
    info_lines = [
        l for l in lines
        if 5 <= len(l) <= 200
    ]

    text = "\n".join(info_lines)

    # ✅ 1️⃣ 统一标准号分隔符
    text = (
        text
        .replace("—", "-")   # em dash
        .replace("–", "-")   # en dash
        .replace("－", "-")  # 全角减号
    )

    # ✅ 2️⃣ 去除中文字符之间的空格
    zh = r'[\u4e00-\u9fff]'
    pattern = re.compile(f'({zh})\\s+({zh})')

    while pattern.search(text):
        text = pattern.sub(r'\1\2', text)

    return text + "\n"