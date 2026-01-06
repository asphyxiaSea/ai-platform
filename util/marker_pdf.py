import io
import json
import requests
from typing import Any, Optional, Union

def extract_pdf(
    *,
    pdf: Union[str, io.BytesIO],
    config: Optional[dict[str, Any]],
) -> str:
    url = "http://localhost:8004/marker-pdf/extract"

    if config is None:
        config = {
            "output_format": "markdown",
            "disable_image_extraction":True
        }
    # 统一成 BytesIO
    if isinstance(pdf, str):
        with open(pdf, "rb") as f:
            pdf_io = io.BytesIO(f.read())
        filename = pdf.split("/")[-1]
    else:
        pdf_io = pdf
        filename = "input.pdf"

    resp = requests.post(
        url,
        files={
            "file": (filename, pdf_io, "application/pdf"),
        },
        data={
            "config": json.dumps(config),
        },
        timeout=60,
    )

    resp.raise_for_status()
    return resp.json()["text"]