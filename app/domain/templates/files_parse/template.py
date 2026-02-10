from app.domain.tasks.task import Task, TaskStep
from app.domain.tasks.files_parse_steps.pdf_preprocess_step import PdfPreprocessStep
from app.domain.tasks.files_parse_steps.marker_step import MarkerStep
from app.domain.tasks.files_parse_steps.paddle_step import PaddleStep
from app.domain.tasks.files_parse_steps.text_preprocess_step import TextPreprocessStep
from app.domain.tasks.files_parse_steps.llm_extract_step import LLMExtractStep
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
