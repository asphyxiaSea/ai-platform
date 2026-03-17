from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from langchain_app.workflows.pdf_structured.nodes import (
    extract_pdf_text_node,
    structured_output_node,
)
from langchain_app.workflows.pdf_structured.state import PdfStructuredState


def build_pdf_structured_graph():
    graph_builder = StateGraph(PdfStructuredState)
    graph_builder.add_node("extract_pdf_text", extract_pdf_text_node)
    graph_builder.add_node("structured_output", structured_output_node)

    graph_builder.add_edge(START, "extract_pdf_text")
    graph_builder.add_edge("extract_pdf_text", "structured_output")
    graph_builder.add_edge("structured_output", END)

    return graph_builder.compile()
