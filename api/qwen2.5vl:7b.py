import requests
from util.image_to_base64 import image_to_base64

img_b64 = image_to_base64("kaohe.jpg")

url = "http://localhost:8001/api/chat"
payload = {
    "model": "qwen2.5vl:7b",
    "messages": [
        {"role": "user", 
         "content": "图里有什么？",
          "images": [img_b64]
         }
    ],
    "stream": False
}

# 发送 POST 请求
response = requests.post(url, json=payload, timeout=300)
response.raise_for_status()  # 出现错误会抛异常

# 获取模型返回内容
data = response.json()
print(data["message"]["content"])