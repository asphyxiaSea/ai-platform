from app.domain.templates.llm_chat.config import LLMTaskConfig, LLMTaskMode
from app.domain.tasks.llm_steps.llm_chat_step import LLMChatStep
from app.domain.tasks.llm_steps.llm_multimodal_step import LLMMultimodalStep
from app.domain.tasks.task import Task, TaskStep


def build_llm_task(config: LLMTaskConfig) -> Task:
    steps: list[TaskStep] = []

    step = (
        LLMMultimodalStep(config)
        if config.task_mode == LLMTaskMode.MULTIMODAL
        else LLMChatStep(config)
    )
    steps.append(step)

    return Task(
        name="llm",
        steps=steps,
    )
