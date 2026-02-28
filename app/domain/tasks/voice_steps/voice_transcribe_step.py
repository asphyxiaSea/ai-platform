from app.domain.errors import InvalidRequestError
from app.domain.resources.context import TaskContext
from app.domain.templates.voice_transcribe.config import VoiceTaskConfig
from app.infra.funasr_client import funasr_transcribe


class VoiceTranscribeStep:
    def __init__(self, config: VoiceTaskConfig) -> None:
        self._config = config

    async def execute(self, context: TaskContext) -> None:
        if not context.file_items:
            raise InvalidRequestError(message="No files provided")
        file_item = context.file_items[0]
        text = await funasr_transcribe(
            file_path=file_item.path or "",
            model_key=self._config.model_key,
        )
        context.result = {"text": text}
