from typing import List
from pydantic import BaseModel
from app.domain.task_config_factory import TaskConfig
from app.service.llm_service import call_ollama
from app.infra.marker_client import extract_file
from app.domain.file_item import FileItem


async def marker_services(
    taskconfig: TaskConfig,
    file_items: list[FileItem],
) -> dict[str, List[BaseModel]]:

    results: List[BaseModel] = []

    for file_item in file_items:
        # 1. marker → text
        text = await extract_file(file_item=file_item, marker=taskconfig.marker)

        # 3. text → LLM
        result = await call_ollama(taskconfig=taskconfig, text=text)
        results.append(result)

    # 当前逻辑：只取第一个（如果这是你 schema 设计决定的）
    return {
        "results": results  # 这里定义的键名要与输出变量名一致
    }

