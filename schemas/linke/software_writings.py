from pydantic import BaseModel, Field
from typing import List

class SoftwareWritings(BaseModel):
    """
    你是一个中文软件著作权信息结构化抽取助手。
    不要输出任何解释、说明、Markdown 或多余文本。
    不要输出 Schema 中未定义的字段。
    """

    software_name: str = Field(
        "",
        description="软件名称"
    )

    registration_number: str = Field(
        "",
        description="登记号（软件著作权登记号）,输出格式如:2023SR0764084"
    )

    acquisition_method: str = Field(
        "",
        description="权利取得方式,例如:原始取得、继受取得"
    )

    development_completion_date: str = Field(
        "",
        description="开发完成日期,输出格式如:2023-05-20"
    )

    registration_date: str = Field(
        "",
        description="登记日期,输出格式如:2023-06-15"
    )

    copyright_holders: List[str] = Field(
        default_factory=list,
        description="著作权人列表,按原文正常阅读顺序提取并存储, 数组中每个字符串不包含空格"
    )