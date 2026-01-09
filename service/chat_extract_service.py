from schemas.registry import SCHEMA_REGISTRY
from domain.task_config import TaskMode
from domain import FileItem
from service.marker_service import marker_services


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