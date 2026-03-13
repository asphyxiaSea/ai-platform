from app.domain.errors import UnsupportedOperationError
from app.domain.tasks.sam3_steps.sam3_segment_step import Sam3SegmentStep
from app.domain.tasks.task import Task, TaskStep
from app.domain.templates.sam3.config import Sam3TaskConfig, Sam3TaskMode


def build_sam3_task(config: Sam3TaskConfig) -> Task:
    steps: list[TaskStep] = []

    if config.task_mode == Sam3TaskMode.SEGMENT_INSTANCE_TEXTS:
        steps.append(
            Sam3SegmentStep(
                config_data=config.reference_config,
                output_key="reference_result",
            )
        )
        steps.append(
            Sam3SegmentStep(
                config_data=config.target_config,
                output_key="target_result",
            )
        )
    else:
        raise UnsupportedOperationError(
            message="未知的任务模式",
            detail=str(config.task_mode),
        )

    return Task(
        name="sam3",
        steps=steps,
    )
