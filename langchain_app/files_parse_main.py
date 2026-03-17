from __future__ import annotations

from app.domain.file_item import FileItem
from app.domain.templates.files_parse.config import FilesTaskConfig

from langchain_app.application.graphs.files_parse.runner import run_files_parse_graph


async def run_files_parse(
    *,
    task_config: FilesTaskConfig,
    file_items: list[FileItem],
    include_trace: bool = False,
) -> dict:
    """Run files_parse workflow mirrored from app legacy pipeline."""
    return await run_files_parse_graph(
        config=task_config,
        file_items=file_items,
        include_trace=include_trace,
    )
