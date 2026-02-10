from app.domain.templates.llm_chat.config import LLMTaskConfig, LLMTaskMode
from app.domain.errors import UnsupportedOperationError
from app.domain.tasks.llm_steps.multimodal import MultimodalLLMStep
from app.domain.tasks.task import Task, TaskStep


def build_llm_task(config: LLMTaskConfig) -> Task:
    steps: list[TaskStep] = []

    if config.task_mode == LLMTaskMode.MULTIMODAL:
        steps.append(MultimodalLLMStep(config))
    else:
        raise UnsupportedOperationError(
            message="未知的任务模式",
            detail=str(config.task_mode),
        )

    return Task(
        name="llm",
        steps=steps,
    )
