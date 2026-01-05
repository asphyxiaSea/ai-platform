from schemas.registry import SCHEMA_REGISTRY
from schemas.taskconfig import TaskMode
from service.multimodal_service import chat_multimodal_images_services,chat_multimodal_pdfs_services
from service.text_service import chat_texts_pdfs_services
from service.text_chunk_service import chat_text_pdfs_service
from service.multimodal_chunk_service import chat_pdfs_images_services


async def chat_extract_service(
    *,
    schema_name: str,
    image_bytes_list: list[bytes],
    pdf_bytes_list: list[bytes],
):
    # 获取schema任务配置
    taskconfig = SCHEMA_REGISTRY.get(schema_name)
    if not taskconfig:
        raise ValueError(f"Unknown schema: {schema_name}")

    # -------- task 分配 --------
    # -------- PDF转纯文本 --------
    if taskconfig.task_mode == TaskMode.PDFTOTEXT:
        if not pdf_bytes_list:
            raise ValueError("This schema requires pdf input")
        return chat_texts_pdfs_services(
            taskconfig=taskconfig,
            pdf_bytes_list=pdf_bytes_list,
        )
    # -------- image多模态 --------
    elif taskconfig.task_mode == TaskMode.IMAGE:
        if not image_bytes_list:
            raise ValueError("This schema requires image input")
        return chat_multimodal_images_services(
            taskconfig=taskconfig,
            image_bytes_list=image_bytes_list,
        )
    # -------- pdftoimage多模态 --------
    elif taskconfig.task_mode == TaskMode.PDFTOIMAGE:
        if not pdf_bytes_list:
            raise ValueError("This schema requires pdf input")
        return chat_multimodal_pdfs_services(
            taskconfig=taskconfig,
            pdf_bytes_list=pdf_bytes_list,
        )
    # -------- PDF转纯文本 + image多模态 --------
    elif taskconfig.task_mode == TaskMode.PDFTOTEXTANDIAMGE:
        if pdf_bytes_list:
            return chat_texts_pdfs_services(
                taskconfig=taskconfig,
                pdf_bytes_list=pdf_bytes_list,
            )
        elif image_bytes_list: 
            return chat_multimodal_images_services(
                taskconfig=taskconfig,
                image_bytes_list=image_bytes_list,
            )
    # -------- PDF转纯文本+分页 --------  
    elif taskconfig.task_mode == TaskMode.PDFTOTEXTBYCHUNK:
        if not pdf_bytes_list:
            raise ValueError("This schema requires pdf input")
        return chat_text_pdfs_service(
            taskconfig=taskconfig,
            pdf_bytes_list=pdf_bytes_list,
        )
    # -------- PDF转纯图像+分页 --------  
    elif taskconfig.task_mode == TaskMode.PDFTOIMAGEBYCHUNK:
        if not pdf_bytes_list:
            raise ValueError("This schema requires pdf input")
        return chat_pdfs_images_services(
            taskconfig=taskconfig,
            pdf_bytes_list=pdf_bytes_list,
        )