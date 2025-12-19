from typing import Dict, Type
from pydantic import BaseModel

from .monograph import MonoGraph

SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {
    "MonoGraph": MonoGraph,
}