from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict

# ===== 进程启动时执行一次 =====

MODEL_DICT = create_model_dict(device="cuda")

CONVERTER = PdfConverter(
    artifact_dict=MODEL_DICT,
    config={"langs": ["Chinese"]}
)