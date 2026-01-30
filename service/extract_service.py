import asyncio
from domain.task_config_factory import TaskConfig, TaskMode
from domain.file_item import FileItem
from domain.preprocess import pdf_preprocess
from service.marker_service import marker_services
from service.paddle_service import paddle_services


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

async def extract_service(
    *,
    taskconfig: TaskConfig,
    file_items: list[FileItem],
):
    file_items = await _apply_pdf_preprocess(
        file_items=file_items,
        preprocess=taskconfig.preprocess,
    )
    # -------- task 分配 --------
    # -------- files->marker->LLM --------
    if taskconfig.task_mode == TaskMode.FILESTOTEXTBYMARKER:
        if not file_items:
            raise ValueError("This schema requires files input")
        return await marker_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )
    # -------- files->paddle->LLM --------
    if taskconfig.task_mode == TaskMode.FILESTOTEXTBYPADDLE:
        if not file_items:
            raise ValueError("This schema requires files input")
        return await paddle_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )