from pydantic import BaseModel, Field
from typing import List, Optional, Literal
class ResearchAwards(BaseModel):
    """
    你是一个中文科研奖励信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """
    achievement_name: Optional[str] = Field(
        None,
        description="成果名称"
    )
    award_type: Optional[str] = Field(
        None,
        description="奖励类型，例如‘科技技术进步奖’、‘自然科学奖’"
    )
    award_status: Optional[Literal[1, 2]]= Field(
        None,
        description="奖励状态，例如：1=申报、2=获奖"
    )
    award_level: Optional[str] = Field(
        None,
        description="奖励等级，例如‘一等奖’、‘二等奖’等。表示奖励的等级或荣誉程度。"
    )
    Awardee: Optional[List[str]] = Field(
        default_factory=list,
        description="获奖者列表，包含所有参与该奖项申报或获得该奖项的人员姓名。"
    )
    application_date: Optional[str] = Field(
        None,
        description="时间，输出格式如:2020-05"
    )