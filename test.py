from marker.output import text_from_rendered
from io import BytesIO
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.renderers.markdown import MarkdownRenderer
from schemas.registry import SCHEMA_REGISTRY

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
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

    variety_status: Optional[int] = Field(
        None,
        description=(
        "品种状态代码。"
        "只能返回一个整数，不要返回文字。"
        "取值范围："
        "1=申请，2=授权，3=转让"
        )
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

pdf_path = "assets/植物新品种权证书(赤云相思）.jpg"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

pdf_stream = BytesIO(pdf_bytes)

# 指向本地 Ollama 服务
client = OpenAI(
    base_url='http://localhost:8001/v1',
    api_key='ollama', # 随便填，不能为空
)

import base64

def encode_image_to_base64(image_path):
    """将本地图片文件转换为 base64 字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
# 1. 准备图片路径
path_to_image = pdf_path
base64_image = encode_image_to_base64(path_to_image)

completion = client.beta.chat.completions.parse(
    model="qwen3-vl:latest", # 确保你已经 ollama pull 了这个模型
    messages=[
        {"role": "user", 
         "content": [
            {
                "type": "text", 
                "text": "提取图中内容"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]},

    ],
    response_format=NewVarieties,
)

print(completion.choices[0].message.content)