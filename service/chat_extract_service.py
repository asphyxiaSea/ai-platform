from schemas.registry import SCHEMA_REGISTRY
from domain.task_config import TaskMode
from service.marker_service import marker_services
from domain import FileItem
from service.multimodal_service import chat_multimodal_images_services,chat_multimodal_pdfs_services
from service.text_chunk_service import chat_text_pdfs_service
from service.multimodal_chunk_service import chat_pdfs_images_services


async def chat_extract_service(
    *,
    schema_name: str,
    file_items: list[FileItem],
):
    # 获取schema任务配置
    taskconfig = SCHEMA_REGISTRY.get(schema_name)
    if not taskconfig:
        raise ValueError(f"Unknown schema: {schema_name}")

    # -------- task 分配 --------
    # -------- files->marker->LLM --------
    if taskconfig.task_mode == TaskMode.FILESTOTEXTBYMARKER:
        if not file_items:
            raise ValueError("This schema requires files input")
        return marker_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )