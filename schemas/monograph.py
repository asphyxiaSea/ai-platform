from pydantic import BaseModel

class MonoGraph(BaseModel):
    name: str
    time: str