from domain.task_config_factory import TaskConfig, TaskMode
from domain import FileItem
from service.marker_service import marker_services
from service.paddle_service import paddle_services

async def extract_service(
    *,
    taskconfig: TaskConfig,
    file_items: list[FileItem],
):
    # -------- task 分配 --------
    # -------- files->marker->LLM --------
    if taskconfig.task_mode == TaskMode.FILESTOTEXTBYMARKER:
        if not file_items:
            raise ValueError("This schema requires files input")
        return marker_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )
    # -------- files->paddle->LLM --------
    if taskconfig.task_mode == TaskMode.FILESTOTEXTBYPADDLE:
        if not file_items:
            raise ValueError("This schema requires files input")
        return paddle_services(
            taskconfig=taskconfig,
            file_items=file_items,
        )