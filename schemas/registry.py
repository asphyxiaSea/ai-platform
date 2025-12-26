from typing import Dict
from .linke.monograph import MonoGraph
from .linke.patent import Patent
from .linke.new_varieties import NewVarieties
from .linke.software_writings import SoftwareWritings
from .linke.research_awards import ResearchAwards
from .linke.paper import Paper
from .linke.improved_variety import ImprovedVariety
from .linke.standard import Standard
from .taskconfig import TaskConfig, InputMode

SCHEMA_REGISTRY: Dict[str, TaskConfig] = {
    "Patent": TaskConfig(
        schema=Patent,
    ),
    "MonoGraph": TaskConfig(
        schema=MonoGraph,
    ),
    "NewVarieties": TaskConfig(
        schema=NewVarieties,
        input_mode=InputMode.IMAGE,
    ),
    "SoftwareWritings": TaskConfig(
        schema=SoftwareWritings,
    ),
    "ResearchAwards": TaskConfig(
        schema=ResearchAwards,
        input_mode=InputMode.PDFTOTEXTANDIAMGE,
    ),
    "Paper": TaskConfig(
        schema=Paper,
    ),
    "ImprovedVariety": TaskConfig(
        schema=ImprovedVariety,
        input_mode=InputMode.IMAGE,
    ),
    "Standard": TaskConfig(
        schema=Standard,
    ),
}