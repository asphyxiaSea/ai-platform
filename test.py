import asyncio
import httpx


async def test_ollama():
    url = "http://localhost:8001/api/chat"  # 如果不通换成 11434

    payload = {
        "model": "gemma3:12b",  # 改成你本地真实模型名
        "messages": [
            {"role": "user", "content": "你好"}
        ],
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload)

        print("状态码:", resp.status_code)
        print("返回内容:")
        print(resp.text)


if __name__ == "__main__":
    asyncio.run(test_ollama())