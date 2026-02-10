from io import BytesIO
import re
from pypdf import PdfReader, PdfWriter
from app.domain.resources.file_item import FileItem


def pdf_preprocess(
    file_item: FileItem,
    preprocess: dict | None,
) -> FileItem:
    """PDF 进入模型前处理（页码裁剪）"""

    page_range = (preprocess and preprocess.get("page_range"))
    if not isinstance(page_range, str):
        return file_item

    reader = PdfReader(BytesIO(file_item.data))
    page_count = len(reader.pages)
    if page_count <= 0:
        return file_item

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
        return file_item

    writer = PdfWriter()
    for i in sorted(pages):
        writer.add_page(reader.pages[i])

    out = BytesIO()
    writer.write(out)
    data = out.getvalue()

    if file_item.path:
        with open(file_item.path, "wb") as f:
            f.write(data)

    return FileItem(
        filename=file_item.filename,
        content_type=file_item.content_type,
        data=data,
        path=file_item.path,
        language=file_item.language,
    )
