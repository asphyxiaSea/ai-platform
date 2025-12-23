from pydantic import BaseModel

class MonoGraph(BaseModel):
    monograph_name: str  = ""
    press: str  = ""
    publication_time: str  = ""
    ISBN: str  = ""
    word_count: str  = ""
