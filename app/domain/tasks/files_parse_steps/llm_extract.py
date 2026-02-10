from app.domain.capabilities.llm.build_llm_prompte import build_ollama_messages
from app.domain.templates.files_parse.config import FilesTaskConfig
from app.infra.llm_client import structured_output


class LLMExtractStep:
    def __init__(self, config: FilesTaskConfig) -> None:
        self.config = config

    async def execute(self, context):
        results = []
        for text in context.texts or []:
            messages = build_ollama_messages(
                taskconfig=self.config,
                text=text,
            )
            result = await structured_output(
                model=self.config.model,
                schema=self.config.schema,
                messages=messages,
                temperature=self.config.temperature,
            )
            results.append(result)

        context.result = {"results": results}
