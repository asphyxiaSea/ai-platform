from pdf2image import convert_from_bytes
from PIL import Image
import base64
import io
def pil_to_base64(img: Image.Image, quality=85) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def pdf_bytes_to_base64_images(
    pdf_bytes: bytes,
    dpi: int = 200,
    quality: int = 85,
):
    images = convert_from_bytes(
        pdf_bytes,
        dpi=dpi,
        fmt="jpeg",
    )

    return [pil_to_base64(img, quality) for img in images]