from app.domain.templates.llm_chat.config import LLMTaskConfig
from app.domain.capabilities.llm.build_llm_prompte import (
    build_multimodal_ollama_messages,
)
from app.domain.resources.context import TaskContext
from app.infra.llm_client import structured_output
from app.util.pdf_utils import image_bytes_to_base64


class MultimodalLLMStep:
    def __init__(self, config: LLMTaskConfig) -> None:
        self._config = config

    async def execute(self, context: TaskContext) -> None:
        image_base64_list = [
            image_bytes_to_base64(file_item.data) for file_item in context.file_items
        ]
        messages = build_multimodal_ollama_messages(
            taskconfig=self._config,
            image_base64_list=image_base64_list,
        )
        context.result = await structured_output(
            model=self._config.vl_model,
            schema=self._config.schema,
            messages=messages,
            temperature=self._config.temperature,
        )
