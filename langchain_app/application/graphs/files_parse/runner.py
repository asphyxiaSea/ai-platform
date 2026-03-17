from __future__ import annotations

from uuid import uuid4

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from app.domain.file_item import FileItem
from app.domain.templates.files_parse.config import FilesTaskConfig

from langchain_app.application.graphs.files_parse.graph import build_files_parse_graph
from langchain_app.application.graphs.files_parse.state import FilesParseState


async def run_files_parse_graph(
    *,
    config: FilesTaskConfig,
    file_items: list[FileItem],
    thread_id: str | None = None,
    include_trace: bool = False,
) -> dict:
    graph = build_files_parse_graph(config)
    compiled = graph.compile(checkpointer=InMemorySaver())

    initial_state: FilesParseState = {
        "file_items": file_items,
        "texts": [],
        "trace": [],
    }
    runnable_config: RunnableConfig = {
        "configurable": {"thread_id": thread_id or str(uuid4())}
    }
    state = await compiled.ainvoke(initial_state, config=runnable_config)

    result = state.get("result")
    if not isinstance(result, dict):
        result = {"results": []}

    if include_trace:
        result["_trace"] = state.get("trace", [])

    return result
