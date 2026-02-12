from app.domain.capabilities.process.text_preprocess import text_preprocess


class TextPreprocessStep:
    def __init__(self, text_process: dict | None):
        self.text_process = text_process

    async def execute(self, context):
        texts = []
        for text in context.get_output("texts", []):
            final_text = text_preprocess(
                text,
                target_sections=self.text_process.get("target_sections", [])
                if self.text_process
                else None,
            )
            texts.append(final_text)

        context.set_output("texts", texts)
