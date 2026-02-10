from app.domain.errors import UnsupportedOperationError
from app.domain.templates.voice_transcribe.config import (
    VoiceTaskConfig,
    VoiceTaskMode,
)
from app.domain.tasks.task import Task, TaskStep
from app.domain.tasks.voice_steps.transcribe import VoiceTranscribeStep


def build_voice_task(config: VoiceTaskConfig) -> Task:
    steps: list[TaskStep] = []

    if config.task_mode == VoiceTaskMode.TRANSCRIBE:
        steps.append(VoiceTranscribeStep(config))
    else:
        raise UnsupportedOperationError(
            message="未知的任务模式",
            detail=str(config.task_mode),
        )

    return Task(
        name="voice_transcribe",
        steps=steps,
    )
