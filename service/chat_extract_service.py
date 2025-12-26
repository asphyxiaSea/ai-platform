from schemas.registry import SCHEMA_REGISTRY
from schemas.taskconfig import InputMode
from service.multimodal_service import chat_multimodal_images_services,chat_multimodal_pdfs_services
from service.text_service import chat_texts_pdfs_services

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
    if taskconfig.input_mode == InputMode.PDFTOTEXT:
        if not pdf_bytes_list:
            raise ValueError("This schema requires pdf input")
        return chat_texts_pdfs_services(
            taskconfig=taskconfig,
            pdf_bytes_list=pdf_bytes_list,
        )
    # -------- image多模态 --------
    elif taskconfig.input_mode == InputMode.IMAGE:
        if not image_bytes_list:
            raise ValueError("This schema requires image input")
        return chat_multimodal_images_services(
            taskconfig=taskconfig,
            image_bytes_list=image_bytes_list,
        )
    # -------- pdftoimage多模态 --------
    elif taskconfig.input_mode == InputMode.PDFTOIMAGE:
        if not pdf_bytes_list:
            raise ValueError("This schema requires pdf input")
        return chat_multimodal_pdfs_services(
            taskconfig=taskconfig,
            pdf_bytes_list=pdf_bytes_list,
        )
    # -------- PDF转纯文本 + image多模态 --------
    elif taskconfig.input_mode == InputMode.PDFTOTEXTANDIAMGE:
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
        