import io
import json
import requests
from typing import Any,  Union
from pypdf import PdfReader

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

class Marker:
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

    def normalize_page_range(self, page_count: int) -> list[int] | None:
        if not self.page_range or page_count <= 0:
            self.page_range = None
            return None

        safe_pages: list[int] = []

        for p in self.page_range:
            if p < 0:
                p = 0
            elif p >= page_count:
                p = page_count - 1

            safe_pages.append(p)

        self.page_range = sorted(set(safe_pages))
        return self.page_range

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
            invalid = set(self.remove_processors) - set(DEFAULT_PROCESSORS_NAME)
            if invalid:
                raise ValueError(
                    f"Unknown processors in remove_processors: {invalid}"
                )

        # ---- 2️⃣ append 校验 ----
        if self.append_processors:
            invalid = set(self.append_processors) - set(DEFAULT_PROCESSORS)
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
        return processor_list
    

def extract_file(
    *,
    file: Union[str, io.BytesIO],
    marker: Marker | None = None,
) -> str:
    url = "http://localhost:8004/marker/extract"

    # ===== 1️⃣ 统一读取 bytes（唯一事实源）=====
    if isinstance(file, str):
        with open(file, "rb") as f:
            file_bytes = f.read()
        filename = file.split("/")[-1]
    else:
        file.seek(0)
        file_bytes = file.read()
        filename = "input"

    # ===== 2️⃣ 判断类型（PDF / Image）=====
    is_pdf = filename.lower().endswith(".pdf")

    data = {}

    if marker is not None:
        if is_pdf:
            # 👉 PDF：读取真实页数
            reader = PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
        else:
            # 👉 Image：事实是“只有 1 页”
            page_count = 1

            # 可选：强制修正 page_range
            marker.page_range = [0]

        marker.normalize_page_range(page_count)

        data["config"] = json.dumps(
            marker.to_config(),
            ensure_ascii=False
        )

        processor_list = marker.to_processor_list()
        if processor_list is not None:
            data["processor_list"] = json.dumps(
                processor_list,
                ensure_ascii=False
            )

    # ===== 3️⃣ 上传（新的 BytesIO）=====
    resp = requests.post(
        url,
        files={
            "file": (
                filename,
                io.BytesIO(file_bytes),
                "application/octet-stream",
            )
        },
        data=data,
        timeout=200,
    )

    resp.raise_for_status()

    text = resp.json()["text"]
    return text if marker and not marker.filter_noisy else filter_noisy(text)
    


def extract_pdf(
    *,
    pdf: Union[str, io.BytesIO],
    marker: Marker | None = None,
) -> str:
    url = "http://localhost:8004/marker/extract"

    if isinstance(pdf, str):
        with open(pdf, "rb") as f:
            pdf_bytes = f.read()
        filename = pdf.split("/")[-1]
    else:
        pdf.seek(0)
        pdf_bytes = pdf.read()
        filename = "input.pdf"

    data = {}

    if marker is not None:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)

        marker.normalize_page_range(page_count)

        data["config"] = json.dumps(marker.to_config(), ensure_ascii=False)
        processor_list = marker.to_processor_list()
        if processor_list is not None:
            data["processor_list"] = json.dumps(processor_list, ensure_ascii=False)

    # 3️⃣ 上传时也用新的 BytesIO
    resp = requests.post(
        url,
        files={
            "file": (
                filename,
                io.BytesIO(pdf_bytes),
                "application/pdf",
            )
        },
        data=data,
        timeout=200,
    )

    resp.raise_for_status()

    text = resp.json()["text"]
    # print(text)
    return filter_noisy(text) if marker and not marker.filter_noisy else text


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