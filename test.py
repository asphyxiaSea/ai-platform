from marker.output import text_from_rendered
from io import BytesIO
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.processors.order import OrderProcessor
from marker.processors.line_merge import LineMergeProcessor
from marker.processors.text import TextProcessor
from marker.renderers.markdown import MarkdownRenderer

pdf_path = "assets/附件3-2Characterization and discrimination of camellia oil varieties according to fatty acid, squalene, tocopherol, and volatile substance contents by chromatogrtaphy chemometrics.pdf"

def cls_path(cls: type) -> str:
    return f"{cls.__module__}.{cls.__qualname__}"


with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

pdf_stream = BytesIO(pdf_bytes)


# 3. 初始化转换器
# 你可以在这里指定语言

config= {
    "extract_images": False,
    "disable_multiprocessing": True,
    "page_range": [0,1]
}


converter = PdfConverter(
# marker-pdf 的全局配置字典
config=config,
# 模型资源注册表
artifact_dict=create_model_dict(device="cuda:1"),
# （核心）结构化中间结果的处理器链
processor_list=[
    cls_path(OrderProcessor),
    cls_path(LineMergeProcessor),
    cls_path(TextProcessor)
],
# 最终输出格式的渲染器，选择输出什么格式json、markdown等
renderer=cls_path(MarkdownRenderer),
)

# 4. 执行转换
rendered = converter(pdf_stream)

# 5. 提取文本内容
full_text, _, _ = text_from_rendered(rendered)

print(full_text)