from marker.output import text_from_rendered
from io import BytesIO
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.renderers.markdown import MarkdownRenderer
from schemas.registry import SCHEMA_REGISTRY

pdf_path = "assets/附件3-2Characterization and discrimination of camellia oil varieties according to fatty acid, squalene, tocopherol, and volatile substance contents by chromatogrtaphy chemometrics.pdf"

def cls_path(cls: type) -> str:
    return f"{cls.__module__}.{cls.__qualname__}"


with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

pdf_stream = BytesIO(pdf_bytes)


# 3. 初始化转换器
# 你可以在这里指定语言
taskconfig = SCHEMA_REGISTRY.get("Paper")
if not taskconfig:
    raise ValueError(f"Unknown schema: {'Paper'}")
schema = taskconfig.schema


config= {
    "extract_images": False,
    "disable_multiprocessing": True,

}


converter = PdfConverter(
# marker-pdf 的全局配置字典
config=config,
# 模型资源注册表
artifact_dict=create_model_dict(device="cuda:1"),
# （核心）结构化中间结果的处理器链
processor_list =[
    "marker.processors.order.OrderProcessor",
    # "marker.processors.sectionheader.SectionHeaderProcessor",
    "marker.processors.line_merge.LineMergeProcessor",
    "marker.processors.text.TextProcessor",
],
# 最终输出格式的渲染器，选择输出什么格式json、markdown等
renderer=cls_path(MarkdownRenderer),
)

# 4. 执行转换
rendered = converter(pdf_stream)

# 5. 提取文本内容
full_text, _, _ = text_from_rendered(rendered)



# print(full_text)

def keep_only_metadata_blocks(full_text: str) -> str:
    lines = full_text.splitlines()

    # 删除过长和过短的行
    info_lines = [l for l in lines if 5 <= len(l) <= 300]

    return "\n".join(info_lines) + "\n"
print("==== Cleaned Text ====")
print(keep_only_metadata_blocks(full_text))


