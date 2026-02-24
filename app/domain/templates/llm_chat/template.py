from app.domain.templates.llm_chat.config import LLMTaskConfig
from app.domain.tasks.llm_steps.llm_step import LLMStep
from app.domain.tasks.task import Task, TaskStep


def build_llm_task(config: LLMTaskConfig) -> Task:
    steps: list[TaskStep] = []

    steps.append(LLMStep(config))

    return Task(
        name="llm",
        steps=steps,
    )
