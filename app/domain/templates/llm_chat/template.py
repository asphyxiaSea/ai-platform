from app.domain.templates.llm_chat.config import LLMTaskConfig
from app.domain.capabilities.llm.llm_config import LLMTaskMode
from app.domain.errors import UnsupportedOperationError
from app.domain.tasks.llm_steps.llm_step import LLMStep
from app.domain.tasks.task import Task, TaskStep


def build_llm_task(config: LLMTaskConfig) -> Task:
    steps: list[TaskStep] = []

    task_mode = config.llm.task_mode

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
