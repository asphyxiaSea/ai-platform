from app.domain.tasks.task import Task, TaskStep
from app.domain.tasks.files_parse_steps.pdf_preprocess import PdfPreprocessStep
from app.domain.tasks.files_parse_steps.marker import MarkerStep
from app.domain.tasks.files_parse_steps.paddle import PaddleStep
from app.domain.tasks.files_parse_steps.text_preprocess import TextPreprocessStep
from app.domain.tasks.files_parse_steps.llm_extract import LLMExtractStep
from app.domain.templates.files_parse.config import FilesTaskConfig, FilesTaskMode


def build_files_parse_task(config: FilesTaskConfig) -> Task:
    steps: list[TaskStep] = [
        PdfPreprocessStep(config.pdf_process),
    ]

    if config.task_mode == FilesTaskMode.FILESTOTEXTBYMARKER:
        steps.append(MarkerStep(config.marker))
    elif config.task_mode == FilesTaskMode.FILESTOTEXTBYPADDLE:
        steps.append(PaddleStep())
    else:
        raise ValueError(f"Unsupported task mode: {config.task_mode}")

    steps.append(TextPreprocessStep(config.text_process))

    steps.append(LLMExtractStep(config))

    return Task(
        name="files_parse",
        steps=steps,
    )
