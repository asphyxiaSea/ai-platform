from pydantic import BaseModel
from typing import List
class ResearchAwards(BaseModel):
    achievement_name: str = ""
    award_level: str = ""
    award_type: str = ""
    award_grade: str = ""
    contributors: List[str] = []