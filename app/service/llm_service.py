from pydantic import BaseModel
from app.domain.task_config_factory import LLMTaskConfig, LLMTaskMode
from app.domain.build_llm_prompte import build_multimodal_ollama_messages
from app.domain.file_item import FileItem
from app.domain.errors import UnsupportedOperationError
from app.infra.llm_client import structured_output
from app.util.pdf_utils import image_bytes_to_base64

async def multimodal_llm_service(
    taskconfig: LLMTaskConfig,
    file_items: list[FileItem],
) -> BaseModel:
    image_bytes_list = [file_item.data for file_item in file_items]
    image_base64_list = []
    for image_bytes in image_bytes_list:
        image_base64_list.append(image_bytes_to_base64(image_bytes))
    messages = build_multimodal_ollama_messages(
        taskconfig=taskconfig,
        image_base64_list=image_base64_list,
    )
    return await structured_output(
        model=taskconfig.vl_model,
        schema=taskconfig.schema,
        messages=messages,
        temperature=taskconfig.temperature,
    )


async def llm_service(
    *,
    taskconfig: LLMTaskConfig,
    file_items: list[FileItem],
) -> BaseModel:
    if taskconfig.task_mode == LLMTaskMode.MULTIMODAL:
        return await multimodal_llm_service(
            taskconfig=taskconfig,
            file_items=file_items,
        )

    raise UnsupportedOperationError(
        message="未知的任务模式",
        detail=str(taskconfig.task_mode),
    )
