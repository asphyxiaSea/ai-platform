from typing import List
from pydantic import BaseModel, Field

class Paper(BaseModel):
    """
    你是一个中文论文信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    title: str = Field(
        "",
        description="论文题目"
    )

    paper_status: str = Field(
        "",
        description="论文状态，例如：已发表、已录用、在投、预印本"
    )

    doi: str = Field(
        "",
        description="论文 DOI 号，如无则为空字符串"
    )

    journal_name: str = Field(
        "",
        description="期刊名称"
    )

    publish_year: str = Field(
        "",
        description="发表年份，如：2021、2022"
    )

    journal_type: str = Field(
        "",
        description="期刊类型，例如：SCI、EI、核心期刊、普通期刊、会议论文"
    )

    volume_issue_pages: str = Field(
        "",
        description="卷/期/页码信息，如：Vol.12(3):45-52"
    )
    funding_projects: str = Field(
        "",
        description="资助项目名称列表，按原文顺序提取"
    )
    authors: List[str] = Field(
        default_factory=list,
        description="作者列表，按论文署名顺序提取"
    )