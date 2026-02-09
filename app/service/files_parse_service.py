import asyncio
from pydantic import BaseModel
from app.domain.task_config_factory import FilesTaskConfig, FilesTaskMode
from app.domain.file_item import FileItem
from app.domain.preprocess import pdf_preprocess
from app.domain.postprocess import text_postprocess
from app.domain.errors import UnsupportedOperationError
from app.infra.marker_client import extract_file as marker_extract_file
from app.infra.paddle_client import extract_file as paddle_extract_file
from app.domain.build_llm_prompting import call_ollama


async def _apply_pdf_preprocess(
    file_items: list[FileItem],
    preprocess: dict | None,
) -> list[FileItem]:
    if not file_items:
        return []

    processed: list[FileItem] = []
    for file_item in file_items:
        if file_item.content_type == "application/pdf":
            data = await asyncio.to_thread(
                pdf_preprocess,
                pdf_bytes=file_item.data,
                preprocess=preprocess,
            )
            processed.append(
                FileItem(
                    filename=file_item.filename,
                    content_type=file_item.content_type,
                    data=data,
                    language=file_item.language,
                )
            )
        else:
            processed.append(file_item)

    return processed


async def _marker_services(
    taskconfig: FilesTaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    results: list[BaseModel] = []

    for file_item in file_items:
        # 1. marker -> text
        text = await marker_extract_file(
            file_item=file_item,
            marker=taskconfig.marker,
        )

        # 2. text -> LLM
        result = await call_ollama(taskconfig=taskconfig, text=text)
        results.append(result)

    return {"results": results}


async def _paddle_services(
    taskconfig: FilesTaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    results: list[BaseModel] = []

    for file_item in file_items:
        # 1. paddle -> text
        text = await paddle_extract_file(file_item=file_item)
        final_text = text_postprocess(
            text,
            target_sections=taskconfig.postprocess.get("target_sections", [])
            if taskconfig.postprocess
            else None,
        )

        # 2. text -> LLM
        result = await call_ollama(taskconfig=taskconfig, text=final_text)
        results.append(result)

    return {"results": results}


async def files_parse_service(
    *,
    taskconfig: FilesTaskConfig,
    file_items: list[FileItem],
):
    file_items = await _apply_pdf_preprocess(
        file_items=file_items,
        preprocess=taskconfig.preprocess,
    )

    if taskconfig.task_mode == FilesTaskMode.FILESTOTEXTBYMARKER:
        if not file_items:
            raise ValueError("This schema requires files input")
        return await _marker_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )

    if taskconfig.task_mode == FilesTaskMode.FILESTOTEXTBYPADDLE:
        if not file_items:
            raise ValueError("This schema requires files input")
        return await _paddle_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )

    raise UnsupportedOperationError(
        message="未知的任务模式",
        detail=str(taskconfig.task_mode),
    )
