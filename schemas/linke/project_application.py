from typing import Optional, List
from pydantic import BaseModel, Field


class ProjectApplication(BaseModel):
    """
    你是一个中文项目申报信息结构化抽取助手,根据html格式的文本信息,提取字段信息。
    只返回符合 Schema 的 JSON，不要输出任何解释、说明或多余文本。
    """

    project_name: Optional[str] = Field(
        None,
        description="项目名称，通常在第一页"
    )

    leading_organization: Optional[str] = Field(
        None,
        description="牵头单位"
    )

    contract_funding: Optional[int] = Field(
        None,
        description="合同经费"
    )

    matching_funding: Optional[int] = Field(
        None,
        description="配套经费"
    )

    total_funding: Optional[int] = Field(
        None,
        description="项目基本情况的项目总经费，一定要从项目基本情况表格中找"
    )

    application_department: Optional[str] = Field(
        None,
        description="申报单位，通常在第一页"
    )

    project_leader: Optional[str] = Field(
        None,
        description="项目组成员信息中的项目负责人，一定要从项目组成员信息表格中找"
    )

    project_duration: Optional[List[str]] = Field(
        None,
        description="项目起止时间，通常在第一页，格式示例：[2023-01-01, 2025-12-01]"
    )

    approval_numbers: List[str] = Field(
        default_factory=list,
        description="合同号或立项文号，可为多个"
    )

    core_team_members: List[str] = Field(
        default_factory=list,
        description="项目组成员信息中的主要人员名单,一定要从项目组成员信息表格中找"
    )