from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from langchain_app.core.settings import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL_NAME,
    DEFAULT_MODEL_PROVIDER,
    DEFAULT_TEMPERATURE,
    OLLAMA_BASE_URL,
)
from langchain_app.infra.clients.paddle_client import paddle_extract_pdf_text
from langchain_app.workflows.pdf_structured.state import PdfStructuredState


@lru_cache(maxsize=1)
def _get_default_model():
    return init_chat_model(
        DEFAULT_MODEL_NAME,
        model_provider=DEFAULT_MODEL_PROVIDER,
        base_url=OLLAMA_BASE_URL,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
    )


async def extract_pdf_text_node(state: PdfStructuredState) -> dict[str, str]:
    text = await paddle_extract_pdf_text(state["pdf_path"])
    return {"extracted_text": text}


async def structured_output_node(state: PdfStructuredState) -> dict[str, dict[str, Any]]:
    schema_model = state["schema_model"]
    system_prompt = state.get(
        "system_prompt",
        "You are an information extraction assistant. Return only schema-conforming JSON.",
    )
    extracted_text = state.get("extracted_text", "")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Please extract structured data from this text:\n\n{extracted_text}"),
    ]

    model = _get_default_model().with_structured_output(schema_model)
    result = await model.ainvoke(messages)

    if isinstance(result, BaseModel):
        payload = result.model_dump()
    elif isinstance(result, dict):
        payload = result
    else:
        payload = {"value": str(result)}

    return {"structured_output": payload}
