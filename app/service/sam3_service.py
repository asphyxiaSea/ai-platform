from app.domain.context import TaskContext
from app.domain.file_item import FileItem
from app.domain.tasks.task_runner import run_task
from app.domain.templates.sam3.config import Sam3TaskConfig
from app.domain.templates.sam3.template import build_sam3_task


async def sam3_service(
    *,
    file_item: FileItem,
    taskconfig: Sam3TaskConfig,
):
    task = build_sam3_task(taskconfig)
    context = TaskContext(file_items=[file_item])
    data = await run_task(task, context)
    return add_tree_heights(
        data=data,
        ruler_real_height=taskconfig.ruler_real_height,
    )


def add_tree_heights(data, ruler_real_height):

    trees = data["target_result"]["results"][0]["boxes"]

    ruler_boxes = data["reference_result"]["results"][0]["boxes"]
    ruler_scores = data["reference_result"]["results"][0]["scores"]

    # 找最高score的ruler
    max_index = ruler_scores.index(max(ruler_scores))
    ruler_box = ruler_boxes[max_index]

    ruler_pixel_height = ruler_box[3] - ruler_box[1]
    if ruler_pixel_height <= 0:
        return data

    heights = []

    for box in trees:
        pixel_height = box[3] - box[1]
        real_height = pixel_height / ruler_pixel_height * ruler_real_height
        heights.append(real_height)

    # 树木高度对应 target_result 中的 boxes。
    data["target_result"]["results"][0]["heights"] = heights

    return data