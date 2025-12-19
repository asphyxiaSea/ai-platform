import requests
from util.pdf_utils import pdf_bytes_to_base64_images

from pydantic import BaseModel, Field

class Book(BaseModel):
    name: str
    time: str

user_prompt = "你是一个专著内容提取小助手。"
url = "http://localhost:8001/api/chat"

with open("assets/专著-热带作物发展史（肉桂发展史）.pdf", "rb") as f:
    pdf_bytes = f.read()

images_bytes = pdf_bytes_to_base64_images(pdf_bytes)

payload = {
    "model": "qwen2.5vl:7b",
    "messages": [
        {"role": "user", 
         "content": user_prompt,
         "images" : images_bytes
         }
    ],
    "stream": False,
    # 强束缚，对提示词有要求，不然会卡死
    "format":Book.model_json_schema()
}


resp = requests.post(url, json=payload, timeout=300)
resp.raise_for_status()

content = resp.json()["message"]["content"]

book = Book.model_validate_json(content)
print(book)