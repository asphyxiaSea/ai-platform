from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser

# ===== 进程启动时执行一次 =====
MODEL_DICT = create_model_dict(device="cuda:1")

CONVERTER = PdfConverter(
    artifact_dict=MODEL_DICT,
    config={"langs": ["Chinese"]}
)

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