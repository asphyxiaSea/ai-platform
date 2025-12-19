from typing import Dict, Type
from pydantic import BaseModel

from .monograph import MonoGraph
from .patent import Patent

SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {
    "Patent": Patent,
    "MonoGraph": MonoGraph,
}