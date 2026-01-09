from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class ResearchAwards(BaseModel):
    """
    你是一个中文科研奖励信息结构化抽取助手，提取 markdown 格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    award_name: Optional[str] = Field(
        None,
        description="奖励名称"
    )

    award_type: Optional[str] = Field(
        None,
        description="奖励类型，例如：科技进步奖、自然科学奖、技术发明奖"
    )

    award_status: Optional[Literal[1, 2]] = Field(
        None,
        description="奖励状态：1=申报，2=获奖"
    )

    award_level: Literal["国家级", "省部级", "部级"]= Field(
        description="奖励级别，指奖项所属层级，注意有文中有国家这两个字的一般为国家级，例如：国家级、省部级等"
    )

    award_grade: Optional[Literal["特等奖", "一等奖", "二等奖", "三等奖","金奖","银奖","优秀奖"]] = Field(
        None,
        description="奖励等级（等次），例如：特等奖、一等奖、二等奖、三等奖"
    )

    awardees: Optional[List[str]] = Field(
        default_factory=list,
        description="获奖者列表，包含所有参与该奖项申报或获得该奖项的人员姓名"
    )

    application_date: Optional[str] = Field(
        None,
        description="申报或获奖时间，格式如：2020-05"
    )
