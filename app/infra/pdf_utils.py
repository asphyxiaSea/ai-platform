import base64
import io
from typing import List
from pdf2image import convert_from_bytes
from PIL import Image


def pil_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def image_bytes_to_base64(image_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def pdf_bytes_to_base64_images(
    pdf_bytes: bytes,
    dpi: int = 200,
) -> List[str]:
    images = convert_from_bytes(
        pdf_bytes,
        dpi=dpi,
        fmt="jpeg",
    )
    return [pil_to_base64(img) for img in images]
