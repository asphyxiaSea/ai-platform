from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.domain.templates.files_parse.config import FilesTaskConfig

from langchain_app.application.graphs.files_parse.nodes import (
    make_llm_extract_node,
    make_paddle_node,
    make_pdf_preprocess_node,
    make_text_preprocess_node,
)
from langchain_app.application.graphs.files_parse.state import FilesParseState


def build_files_parse_graph(config: FilesTaskConfig):
    graph = StateGraph(FilesParseState)

    graph.add_node("pdf_preprocess", make_pdf_preprocess_node(config))
    graph.add_node("paddle", make_paddle_node())
    graph.add_node("text_preprocess", make_text_preprocess_node(config))
    graph.add_node("llm_extract", make_llm_extract_node(config))

    graph.add_edge(START, "pdf_preprocess")
    graph.add_edge("pdf_preprocess", "paddle")
    graph.add_edge("paddle", "text_preprocess")
    graph.add_edge("text_preprocess", "llm_extract")
    graph.add_edge("llm_extract", END)

    return graph
