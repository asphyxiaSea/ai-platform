from app.domain.tasks.task import Task, TaskStep
from app.domain.tasks.files_parse_steps.pdf_preprocess_step import PdfPreprocessStep
from app.domain.tasks.files_parse_steps.paddle_step import PaddleStep
from app.domain.tasks.files_parse_steps.text_preprocess_step import TextPreprocessStep
from app.domain.tasks.files_parse_steps.llm_extract_step import LLMExtractStep
from app.domain.templates.files_parse.config import FilesTaskConfig


def build_files_parse_task(config: FilesTaskConfig) -> Task:
    steps: list[TaskStep] = [
        PdfPreprocessStep(config.pdf_process),
    ]

    steps.append(PaddleStep())

    steps.append(TextPreprocessStep(config.text_process))

    steps.append(LLMExtractStep(config))

    return Task(
        name="files_parse",
        steps=steps,
    )
