from __future__ import annotations

from time import perf_counter
from typing import Any

from app.domain.context import TaskContext
from app.domain.errors import ExternalServiceError
from app.domain.tasks.files_parse_steps.llm_extract_step import LLMExtractStep
from app.domain.tasks.files_parse_steps.paddle_step import PaddleStep
from app.domain.tasks.files_parse_steps.pdf_preprocess_step import PdfPreprocessStep
from app.domain.tasks.files_parse_steps.text_preprocess_step import TextPreprocessStep
from app.domain.templates.files_parse.config import FilesTaskConfig

from langchain_app.application.graphs.files_parse.state import FilesParseState, TraceItem


def _trace(
    *,
    node: str,
    status: str,
    started_at: float,
    summary: dict[str, Any],
) -> list[TraceItem]:
    return [
        {
            "node": node,
            "status": status,
            "duration_ms": round((perf_counter() - started_at) * 1000, 3),
            "summary": summary,
        }
    ]


def make_pdf_preprocess_node(config: FilesTaskConfig):
    async def pdf_preprocess_node(state: FilesParseState) -> dict[str, Any]:
        started = perf_counter()
        try:
            context = TaskContext(file_items=list(state.get("file_items", [])))
            step = PdfPreprocessStep(config.pdf_process)
            await step.execute(context)
            return {
                "file_items": context.file_items,
                "trace": _trace(
                    node="pdf_preprocess",
                    status="ok",
                    started_at=started,
                    summary={"file_count": len(context.file_items)},
                ),
            }
        except Exception as exc:
            raise ExternalServiceError(
                message="pdf_preprocess node failed",
                detail={"node": "pdf_preprocess", "error": str(exc)},
            ) from exc

    return pdf_preprocess_node


def make_paddle_node():
    async def paddle_node(state: FilesParseState) -> dict[str, Any]:
        started = perf_counter()
        try:
            context = TaskContext(file_items=list(state.get("file_items", [])))
            step = PaddleStep()
            await step.execute(context)
            texts = context.get_output("texts", [])
            return {
                "texts": texts,
                "trace": _trace(
                    node="paddle",
                    status="ok",
                    started_at=started,
                    summary={"text_count": len(texts)},
                ),
            }
        except Exception as exc:
            raise ExternalServiceError(
                message="paddle node failed",
                detail={"node": "paddle", "error": str(exc)},
            ) from exc

    return paddle_node


def make_text_preprocess_node(config: FilesTaskConfig):
    async def text_preprocess_node(state: FilesParseState) -> dict[str, Any]:
        started = perf_counter()
        try:
            context = TaskContext(file_items=[])
            context.set_output("texts", list(state.get("texts", [])))
            step = TextPreprocessStep(config.text_process)
            await step.execute(context)
            texts = context.get_output("texts", [])
            return {
                "texts": texts,
                "trace": _trace(
                    node="text_preprocess",
                    status="ok",
                    started_at=started,
                    summary={"text_count": len(texts)},
                ),
            }
        except Exception as exc:
            raise ExternalServiceError(
                message="text_preprocess node failed",
                detail={"node": "text_preprocess", "error": str(exc)},
            ) from exc

    return text_preprocess_node


def make_llm_extract_node(config: FilesTaskConfig):
    async def llm_extract_node(state: FilesParseState) -> dict[str, Any]:
        started = perf_counter()
        try:
            context = TaskContext(file_items=[])
            context.set_output("texts", list(state.get("texts", [])))
            step = LLMExtractStep(config)
            await step.execute(context)
            result = context.result if isinstance(context.result, dict) else {"results": []}
            count = len(result.get("results", []))
            return {
                "result": result,
                "trace": _trace(
                    node="llm_extract",
                    status="ok",
                    started_at=started,
                    summary={"result_count": count},
                ),
            }
        except Exception as exc:
            raise ExternalServiceError(
                message="llm_extract node failed",
                detail={"node": "llm_extract", "error": str(exc)},
            ) from exc

    return llm_extract_node
