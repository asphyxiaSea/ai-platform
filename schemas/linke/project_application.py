from pydantic import BaseModel, Field


class ProjectApplication(BaseModel):
    """
    你是一个中文项目申报信息结构化抽取助手。
    不要输出任何解释、说明、Markdown 或多余文本。
    """

    项目名称: str = Field()
    牵头单位: str = Field()
    合同经费: int = Field()
    配套经费: int = Field()
    总经费: str = Field()
    申报部门: str = Field()
    项目负责人: str = Field()
    起止时间: list[str] = Field()
    合同号或立项文号: str = Field()
    项目组主要人员: list[str] = Field()