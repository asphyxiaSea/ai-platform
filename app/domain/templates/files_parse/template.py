from app.domain.tasks.task import Task, TaskStep
from app.domain.tasks.files_parse_steps.pdf_preprocess import PdfPreprocessStep
from app.domain.tasks.files_parse_steps.marker import MarkerStep
from app.domain.tasks.files_parse_steps.paddle import PaddleStep
from app.domain.tasks.files_parse_steps.text_preprocess import TextPreprocessStep
from app.domain.tasks.files_parse_steps.llm_extract import LLMExtractStep
from app.domain.templates.files_parse.config import FilesParseConfig


def build_files_parse_task(config: FilesParseConfig) -> Task:
    steps: list[TaskStep] = [
        PdfPreprocessStep(config.pdf_process),
    ]

    if config.parser_backend == "marker":
        steps.append(MarkerStep(config.marker))
    elif config.parser_backend == "paddle":
        steps.append(PaddleStep())
    else:
        raise ValueError(f"Unsupported parser backend: {config.parser_backend}")

    steps.append(TextPreprocessStep(config.text_process))

    steps.append(LLMExtractStep(config))

    return Task(
        name="files_parse",
        steps=steps,
    )
