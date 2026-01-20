from io import BytesIO
import re
from pypdf import PdfReader, PdfWriter

import re
from io import BytesIO
from pypdf import PdfReader, PdfWriter


def pdf_preprocess(
    pdf_bytes: bytes,
    preprocess: dict | None,
) -> bytes:
    """PDF 进入 Paddle 前的前处理（页码裁剪）"""

    page_range = (preprocess and preprocess.get("page_range"))
    if not isinstance(page_range, str):
        return pdf_bytes

    reader = PdfReader(BytesIO(pdf_bytes))
    page_count = len(reader.pages)
    if page_count <= 0:
        return pdf_bytes

    # ---- 页码解析 ----
    pages: set[int] = set()
    for part in re.split(r"[，,]", page_range):
        part = part.strip()
        if not part:
            continue
        try:
            if "-" in part:
                s, e = map(int, part.split("-", 1))
                for p in range(s, e + 1):
                    if 1 <= p <= page_count:
                        pages.add(p - 1)   # PdfReader 是 0-based
            else:
                p = int(part)
                if 1 <= p <= page_count:
                    pages.add(p - 1)
        except ValueError:
            continue
    # ------------------

    if not pages:
        return pdf_bytes

    writer = PdfWriter()
    for i in sorted(pages):
        writer.add_page(reader.pages[i])

    out = BytesIO()
    writer.write(out)
    return out.getvalue()
