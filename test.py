from marker.output import text_from_rendered
from io import BytesIO
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

pdf_path = "assets/桉树人工林土壤质量演变与提升关键技术——获奖个人证书.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

pdf_stream = BytesIO(pdf_bytes)


# 3. 初始化转换器
# 你可以在这里指定语言

config = {
    "output_format": "markdown",
    "page_range": "0-5",
    "disable_image_extraction": True,
    "langs": ["Chinese"]
}
config_parser = ConfigParser(config)

converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(device="cuda:1"),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
    llm_service=config_parser.get_llm_service()
)

# 4. 执行转换
rendered = converter(pdf_stream)

# 5. 提取文本内容
full_text, _, _ = text_from_rendered(rendered)

print(full_text)

