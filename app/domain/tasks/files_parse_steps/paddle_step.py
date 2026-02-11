from app.infra.paddle_client import extract_file


class PaddleStep:
    async def execute(self, context):
        texts = []
        for file_item in context.file_items:
            text = await extract_file(file_item=file_item)
            texts.append(text)
        context.texts = texts
