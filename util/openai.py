from openai import OpenAI
from pydantic import BaseModel
# 指向本地 Ollama 服务
client = OpenAI(
    base_url='http://localhost:8001/v1',
    api_key='ollama',
)


def openai_structure_output(
    *,
    model: str,
    schema: type[BaseModel],
    messages: list,
    temperature: float,
) -> BaseModel:
    
    completion = client.chat.completions.parse(
        model=model,
        messages=messages,
        temperature=temperature,
        response_format=schema,
    )

    msg = completion.choices[0].message

    if msg.parsed is not None:
        return msg.parsed

    raise ValueError("Structured Outputs 解析失败,parsed 为空")

