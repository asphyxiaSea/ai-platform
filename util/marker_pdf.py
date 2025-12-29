from typing import Union,Any
import io

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

PROCESSORS: dict[str, str] = {
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

DEFAULT_PROCESSORS = [
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

        # 3️⃣ 表格（默认开启）
        "table",

        # 4️⃣ 输出
        "text",
        "blank_page",
    ]

class MarkerPDF:
    """
    高性能 PDF → RAG 文本抽取流水线
    - 可控 processor 集
    - 无表格 / 无 LLM
    - 强噪声过滤
    """

    def __init__(
        self,
        device: str = "cuda:1",
        # 提取pdf文件的页码范围
        page_range: list[int] | None = None,
        # 是否提取图片,默认为否
        extract_images: bool = False,
        # 输出格式，默认为 markdown
        output_format: str = "markdown",
        # 忽略的 processor 列表
        ignore_processors: list[str] | None = None,
    ):
        self.device = device
        self.page_range = page_range
        self.extract_images = extract_images
        self.output_format = output_format
        self.ignore_processors = ignore_processors

        self._build_converter()


    def _build_converter(self):

        # ===== 第一层：性能过滤（config）=====
        config: dict[str, Any] = {
            "extract_images": self.extract_images,
            "output_format": self.output_format,
        }
        if self.page_range:
            config["page_range"] = self.page_range

        # ===== 第二层：语义过滤（processors）=====
        processor_list = None
        if self.ignore_processors is None:
            processor_list = [
                PROCESSORS[name]
                for name in DEFAULT_PROCESSORS
            ]
        else:
            processor_list = [
                PROCESSORS[name]
                for name in DEFAULT_PROCESSORS
                if name not in self.ignore_processors
            ]

        # ===== 构建 converter =====
        self.converter = PdfConverter(
            config=config,
            artifact_dict=create_model_dict(device=self.device),
            processor_list=processor_list,
        )


    def extract_text(self,pdf: Union[str, io.BytesIO]) -> str:
        """
        返回干净、可直接用于 RAG 的全文字符串
        """
        rendered = self.converter(pdf)
        text, _, _ = text_from_rendered(rendered)
        # text = keep_only_metadata_blocks(text)
        # print(text)
        return text
    


def keep_only_metadata_blocks(full_text: str) -> str:
    lines = full_text.splitlines()

    info_lines = [
        l for l in lines
        if 5 <= len(l) <= 300
    ]

    return "\n".join(info_lines) + "\n"
