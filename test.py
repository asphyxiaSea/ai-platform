from marker.output import text_from_rendered
from io import BytesIO
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

pdf_path = "assets/附件3-2Characterization and discrimination of camellia oil varieties according to fatty acid, squalene, tocopherol, and volatile substance contents by chromatogrtaphy chemometrics.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

pdf_stream = BytesIO(pdf_bytes)


# 3. 初始化转换器
# 你可以在这里指定语言

config = {
    "output_format": "markdown",
    "page_range": "0",
    "disable_image_extraction": True,
    "langs": ["Chinese"]
}
config_parser = ConfigParser(config)

converter = PdfConverter(
# marker-pdf 的全局配置字典
config=config_parser.generate_config_dict(),
# 模型资源注册表
artifact_dict=create_model_dict(device="cuda"),
# （核心）结构化中间结果的处理器链
processor_list=config_parser.get_processors(),
# 最终输出格式的渲染器，选择输出什么格式json、markdown等
renderer=config_parser.get_renderer(),
# LLM 增强模块（可选）
llm_service=config_parser.get_llm_service()
)

# 4. 执行转换
rendered = converter(pdf_stream)

# 5. 提取文本内容
full_text, _, _ = text_from_rendered(rendered)

print(full_text)

