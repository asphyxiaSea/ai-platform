from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Paper(BaseModel):
    """
    你是一个中文论文信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    title: Optional[str] = Field(
        None,
        description="论文题目,优先使用中文题目。"
    )

    paper_status: Literal[1, 2] = Field(
        2,
        description=(
            "论文状态:1=已录用(仅当文本中明确出现“录用 / accepted”等字样时填写),2=已发表"
        )
    )

    doi: Optional[str] = Field(
        None,
        description="论文DOI号"
    )

    journal_name: Optional[str] = Field(
        None,
        description="期刊名称，优先使用中文期刊名称"
    )

    publish_year: Optional[str] = Field(
        None,
        description="发表年份，如：2021、2022"
    )

    journal_type: Optional[str] = Field(
        None,
        description="期刊类型，例如：SCI、EI、核心期刊、普通期刊、会议论文"
    )

    volume_issue_pages: Optional[str] = Field(
        None,
        description="卷/期/页码信息，如：Vol.12(3):45-52"
    )
    funding_projects: Optional[str] = Field(
        None,
        description="资助项目名称列表，按原文顺序提取"
    )
    authors: Optional[List[str]] = Field(
        default_factory=list,
        description="作者列表，按论文署名顺序提取"
    )

