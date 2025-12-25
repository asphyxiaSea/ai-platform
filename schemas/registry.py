from typing import Dict
from .linke.monograph import MonoGraph
from .linke.patent import Patent
from .linke.new_varieties import NewVarieties
from .linke.software_writings import SoftwareWritings
from .linke.research_awards import ResearchAwards
from .taskconfig import TaskConfig

SCHEMA_REGISTRY: Dict[str, TaskConfig] = {
    "Patent": TaskConfig(
        schema=Patent,
        model="gemma3:latest",
    ),
    "MonoGraph": TaskConfig(
        schema=MonoGraph,
        model="gemma3:latest",
    ),
    "NewVarieties": TaskConfig(
        schema=NewVarieties,
        model="qwen3-vl:latest",
    ),
    "SoftwareWritings": TaskConfig(
        schema=SoftwareWritings,
        model="gemma3:latest",
    ),
    "ResearchAwards": TaskConfig(
        schema=ResearchAwards,
        model="gemma3:latest",
    ),
}