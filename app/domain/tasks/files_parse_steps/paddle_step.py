from app.infra.paddle_client import paddle_extract_file


class PaddleStep:
    async def execute(self, context):
        texts = []
        for file_item in context.file_items:
            text = await paddle_extract_file(file_item=file_item)
            texts.append(text)
        context.set_output("texts", texts)
