from app.infra.marker_client import extract_file


class MarkerStep:
    def __init__(self, marker_config):
        self.marker = marker_config

    async def execute(self, context):
        texts = []
        for file_item in context.file_items:
            text = await extract_file(
                file_item=file_item,
                marker=self.marker,
            )
            texts.append(text)

        context.texts = texts
