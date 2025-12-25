from pydantic import BaseModel, Field
from typing import List
class ResearchAwards(BaseModel):
    """
    你是一个中文科研奖励信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """
    achievement_name: str = Field(
        "",
        description="成果名称"
    )
    award_type: str = Field(
        "",
        description="奖励类型，例如‘科技进步奖’、‘自然科学奖’等。表示奖励的具体内容。"
    )
    award_level: str = Field(
        "",
        description="奖励等级，例如‘一等奖’、‘二等奖’等。表示奖励的等级或荣誉程度。"
    )
    Awardee: List[str] = Field(
        default_factory=list,
        description="获奖者列表，包含所有参与该奖项申报或获得该奖项的人员姓名。"
    )