from app.domain.templates.llm_chat.config import LLMTaskConfig, LLMTaskMode
from app.domain.errors import UnsupportedOperationError
from app.domain.tasks.llm_steps.llm_step import LLMStep
from app.domain.tasks.task import Task, TaskStep


def build_llm_task(config: LLMTaskConfig) -> Task:
    steps: list[TaskStep] = []

    task_mode = LLMTaskMode.MULTIMODAL if config.has_images else LLMTaskMode.CHAT

    if task_mode in {LLMTaskMode.MULTIMODAL, LLMTaskMode.CHAT}:
        steps.append(LLMStep(config))
    else:
        raise UnsupportedOperationError(
            message="未知的任务模式",
            detail=str(task_mode),
        )

    return Task(
        name="llm",
        steps=steps,
    )
