from pydantic import BaseModel, Field
from typing import Optional

class ImprovedVariety(BaseModel):
    """
    你是一个中文良种信息结构化抽取助手。
    你的任务是从 markdown 格式的文本中，提取良种相关信息。

    要求：
    - 只输出 JSON
    - 不要输出任何解释、说明、Markdown 或多余文本
    - 不要输出 Schema 中未定义的字段
    - 无法提取的字段请输出空字符串
    """

    variety_name: str = Field("", description="良种名称")
    species: str = Field("", description="树种")
    variety_level: str = Field("", description="良种等级")
    variety_code: str = Field("", description="良种编号")
    variety_status: Optional[int] = Field(
        None,
        description=(
        "良种状态代码。"
        "只能返回一个整数，不要返回文字。"
        "取值范围："
        "1=原始取得，2=继受取得"
        )
    )
    approval_date: str = Field("", description="认定或审定日期，例如:2022年8月输出2022-08")
    applicant: str = Field("", description="申请人")
    breeder: str = Field("", description="选育人")