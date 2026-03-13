from app.domain.context import TaskContext
from app.domain.errors import InvalidRequestError
from app.infra.sam3_client import sam3_segment_instance_texts


class Sam3SegmentStep:
    def __init__(self, *, config_data: dict, output_key: str) -> None:
        self._config_data = config_data
        self._output_key = output_key

    async def execute(self, context: TaskContext) -> None:
        if not context.file_items:
            raise InvalidRequestError(message="No files provided")

        file_item = context.file_items[0]
        current_result = await sam3_segment_instance_texts(
            file_item=file_item,
            config_data=self._config_data,
        )
        context.set_output(self._output_key, current_result)
        context.result = {
            "reference_result": context.get_output("reference_result"),
            "target_result": context.get_output("target_result"),
        }
