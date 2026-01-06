from typing import Dict
from .linke.monograph import MonoGraph
from .linke.patent import Patent
from .linke.new_varieties import NewVarieties
from .linke.software_writings import SoftwareWritings
from .linke.research_awards import ResearchAwards
from .linke.paper import Paper
from .linke.improved_variety import ImprovedVariety
from .linke.standard import Standard
from .linke.project_application import ProjectApplication
from .taskconfig import TaskConfig, TaskMode

SCHEMA_REGISTRY: Dict[str, TaskConfig] = {
    "Patent": TaskConfig(
        schema=Patent,
    ),
    "MonoGraph": TaskConfig(
        schema=MonoGraph,
    ),
    "NewVarieties": TaskConfig(
        schema=NewVarieties,
        task_mode=TaskMode.IMAGE,
    ),
    "SoftwareWritings": TaskConfig(
        schema=SoftwareWritings,
    ),
    "ResearchAwards": TaskConfig(
        schema=ResearchAwards,
        task_mode=TaskMode.PDFTOTEXTANDIAMGE,
        # markerpdf_config={
        #     "output_format": "markdown"
        # },
    ),
    "Paper": TaskConfig(
        schema=Paper,
        markerpdf_config={
            "page_range": list(range(0, 4)),
    },
    ),
    "ImprovedVariety": TaskConfig(
        schema=ImprovedVariety,
        task_mode=TaskMode.IMAGE,
    ),
    "Standard": TaskConfig(
        schema=Standard,
    ),

    "ProjectApplication": TaskConfig(
        schema=ProjectApplication,
        model="qwen3:latest",
        # task_mode=TaskMode.PDFTOIMAGEBYCHUNK,
        markerpdf_config={
            "page_range": list(range(0, 10)),
        },
    ),
}