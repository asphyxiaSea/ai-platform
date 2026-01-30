from pydantic import BaseModel
from app.domain.task_config_factory import TaskConfig
from app.domain.file_item import FileItem
from app.infra.paddle_client import extract_file
from app.service.llm_service import call_ollama
from app.domain.postprocess import text_postprocess


async def paddle_services(
    taskconfig: TaskConfig,
    file_items: list[FileItem],
) -> dict[str, list[BaseModel]]:
    results: list[BaseModel] = []
    for file_item in file_items:
        # 1. paddle → text
        text = await extract_file(file_item=file_item)
        final_text = text_postprocess(
            text,
            target_sections=taskconfig.postprocess.get("target_sections", [])
            if taskconfig.postprocess
            else None,
        )
        print(final_text)

        # 3. text → LLM
        result = await call_ollama(taskconfig=taskconfig, text=final_text)
        results.append(result)

    return {
        "results": results  # 这里定义的键名要与输出变量名一致
    }



