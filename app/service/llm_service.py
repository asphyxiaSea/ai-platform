from pydantic import BaseModel
from app.domain.task_config_factory import LLMTaskConfig, LLMTaskMode
from app.domain.build_llm_prompte import build_multimodal_messages
from app.domain.file_item import FileItem
from app.domain.errors import UnsupportedOperationError
from app.infra.llm_client import structured_output

async def multimodal_llm_service(
    taskconfig: LLMTaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    results: list[BaseModel] = []
    for file_item in file_items:
        messages = build_multimodal_messages(
            taskconfig=taskconfig,
            image_base64=file_item.data,
        )
        result = await structured_output(
            model=taskconfig.vl_model,
            schema=taskconfig.schema,
            messages=messages,
            temperature=taskconfig.temperature,
        )
        results.append(result)

    return {
        "results": results  # 这里定义的键名要与输出变量名一致
    }


async def llm_service(
    *,
    taskconfig: LLMTaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    if taskconfig.task_mode == LLMTaskMode.MULTIMODAL:
        return await multimodal_llm_service(
            taskconfig=taskconfig,
            file_items=file_items,
        )

    raise UnsupportedOperationError(
        message="未知的任务模式",
        detail=str(taskconfig.task_mode),
    )
