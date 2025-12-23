from typing import Dict, Type
from pydantic import BaseModel

from .monograph import MonoGraph
from .patent import Patent
from .new_varieties import NewVarieties
from .software_writings import SoftwareWritings
from .research_awards import ResearchAwards

SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {
    "Patent": Patent,
    "MonoGraph": MonoGraph,
    "NewVarieties": NewVarieties,
    "SoftwareWritings": SoftwareWritings,
    "ResearchAwards": ResearchAwards,
}