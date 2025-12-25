from pydantic import BaseModel, Field
from typing import List

class NewVarieties(BaseModel):
    """
    你是一个中文新品种信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    variety_name: str = Field(
        "",
        description="品种名称"
    )

    variety_right_number: str = Field(
        "",
        description="品种权号（植物新品种权号）"
    )

    variety_status: str = Field(
        "",
        description="品种状态，例如：申请中、已授权、已公告、已失效"
    )

    application_date: str = Field(
        "",
        description="申请日期,输出格式如：2022-03-15、2022-03"
    )

    grant_date: str = Field(
        "",
        description="授权日期,输出格式如：2022-03-15、2022-03;未授权则为空字符串"
    )

    variety_right_holder: str = Field(
        "",
        description="品种权人（单位或个人）"
    )

    breeders: List[str] = Field(
        default_factory=list,
        description="选育人列表，按原文顺序提取"
    )