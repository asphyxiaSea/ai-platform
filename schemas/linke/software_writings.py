from pydantic import BaseModel, Field
from typing import List,Optional

class SoftwareWritings(BaseModel):
    """
    你是一个中文软件著作权信息结构化抽取助手，提取markdown格式的文本信息。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    software_name: Optional[str] = Field(
        None,
        description="软件名称"
    )

    registration_number: Optional[str] = Field(
        None,
        description="登记号（软件著作权登记号）,输出格式如:2023SR0764084"
    )

    acquisition_method: Optional[int] = Field(
        None,
        description=(
        "权利取得方式代码。"
        "只能返回一个整数，不要返回文字。"
        "取值范围："
        "1=原始取得，2=继受取得"
        )
    )

    development_completion_date: Optional[str] = Field(
        None,
        description="开发完成日期,输出格式如:2023-05-20"
    )

    registration_date: Optional[str] = Field(
        None,
        description="登记日期,输出格式如:2023-06-15"
    )

    copyright_holders: Optional[List[str]] = Field(
        default_factory=list,
        description="著作权人列表,按原文正常阅读顺序提取并存储, 数组中每个字符串不包含空格"
    )