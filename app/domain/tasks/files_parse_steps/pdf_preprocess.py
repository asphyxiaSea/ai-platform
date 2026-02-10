import asyncio
from app.domain.capabilities.process.pdf_preprocess import pdf_preprocess
from app.domain.resources.file_item import FileItem


class PdfPreprocessStep:
    def __init__(self, pdf_process: dict | None):
        self.pdf_process = pdf_process

    async def execute(self, context):
        processed: list[FileItem] = []

        for file_item in context.file_items:
            if file_item.content_type == "application/pdf":
                updated_item = await asyncio.to_thread(
                    pdf_preprocess,
                    file_item=file_item,
                    preprocess=self.pdf_process,
                )
                processed.append(updated_item)
            else:
                processed.append(file_item)

        context.file_items = processed
