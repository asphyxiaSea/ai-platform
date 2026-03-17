from __future__ import annotations

import json
import os
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, Form, UploadFile

from langchain_app.api.models import SchemaPayload
from langchain_app.application.pipelines.pdf_structured_pipeline import (
    run_pdf_structured_pipeline,
)
from langchain_app.core.errors import ExternalServiceError, InvalidRequestError
from langchain_app.domain.schemas import create_schema_model

router = APIRouter(tags=["langchain-app"])


@router.post("/files/parse")
async def parse_pdf_to_structured(
    file: UploadFile = File(...),
    schema: str = Form(...),
    system_prompt: str = Form(default=""),
) -> dict:
    if file.content_type != "application/pdf":
        raise InvalidRequestError(message="仅支持 PDF 文件", detail=file.content_type)

    try:
        payload = SchemaPayload.model_validate(json.loads(schema))
    except Exception as exc:
        raise InvalidRequestError(message="schema 格式错误", detail=str(exc)) from exc

    schema_model = create_schema_model(
        schema_name=payload.schema_name,
        fields=payload.fields,
    )

    temp_path = ""
    try:
        content = await file.read()
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        result = await run_pdf_structured_pipeline(
            pdf_path=temp_path,
            schema_model=schema_model,
            system_prompt=system_prompt,
        )
        return {
            "results": [result.get("structured_output", {})],
            "extracted_text": result.get("extracted_text", ""),
        }
    except InvalidRequestError:
        raise
    except Exception as exc:
        raise ExternalServiceError(message="PDF 结构化提取失败", detail=str(exc)) from exc
    finally:
        await file.close()
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
