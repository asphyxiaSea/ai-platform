# from typing import Dict
# from .linke.monograph import MonoGraph
# from .linke.patent import Patent
# from .linke.new_varieties import NewVarieties
# from .linke.software_writings import SoftwareWritings
# from .linke.research_awards import ResearchAwards
# from .linke.paper import Paper
# from .linke.improved_variety import ImprovedVariety
# from .linke.standard import Standard
# from .linke.project_application import ProjectApplication
# from domain.task_config import TaskConfig,TaskMode
# from domain import Marker

# SCHEMA_REGISTRY: Dict[str, TaskConfig] = {
#     "defalt":TaskConfig(
#     ),
#     "Patent": TaskConfig(
#         schema=Patent,
#     ),
#     "MonoGraph": TaskConfig(
#         schema=MonoGraph,
#     ),
#     "NewVarieties": TaskConfig(
#         schema=NewVarieties,
#         task_mode=TaskMode.FILESTOTEXTBYMARKER,
#     ),
#     "SoftwareWritings": TaskConfig(
#         schema=SoftwareWritings,
#     ),
#     "ResearchAwards": TaskConfig(
#         schema=ResearchAwards,
#     ),
#     "Paper": TaskConfig(
#         schema=Paper,
#         task_mode=TaskMode.FILESTOTEXTBYMARKER,
#         marker=Marker(
#             page_range=list(range(0, 4)),
#             filter_noisy=True,
#         )
#     ),
#     "ImprovedVariety": TaskConfig(
#         schema=ImprovedVariety,
#     ),
#     "Standard": TaskConfig(
#         schema=Standard,
#         marker=Marker(
#             filter_noisy=True,
#             page_range=list(range(0, 4)),
#         )
#     ),

#     "ProjectApplication": TaskConfig(
#         schema=ProjectApplication,
#         model="qwen3:latest",
#     ),
# }