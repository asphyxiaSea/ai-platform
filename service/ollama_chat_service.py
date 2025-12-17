from typing import List,Optional,Dict, Any
from fastapi import HTTPException
import requests
from util.pdf_utils import pdf_bytes_to_base64_images,image_bytes_to_base64

def chat_text_only(model: str, prompt: str) -> str:
    return _call_ollama(
        model=model,
        prompt=prompt
    )

def chat_with_images(
    model: str,
    prompt: str,
    images_bytes: List[bytes]
) -> str:
    if not images_bytes:
        raise HTTPException(400, "images is required")

    images_b64 = [
        image_bytes_to_base64(b) for b in images_bytes
    ]

    return _call_ollama(
        model=model,
        prompt=prompt,
        images=images_b64
    )

def chat_with_pdf(model: str, prompt: str, pdf_bytes: bytes) -> str:
    images_bytes = pdf_bytes_to_base64_images(pdf_bytes)

    if not images_bytes:
        raise HTTPException(400, "PDF contains no pages")

    return _call_ollama(
        model=model,
        prompt=prompt,
        images=images_bytes
    )

def _call_ollama(
    model: str,
    prompt: str,
    images: Optional[List[str]] = None
) -> str:
    """
    Ollama 统一调用入口
    """
    message: Dict[str, Any] = {
        "role": "user",
        "content": prompt,
    }

    if images:
        message["images"] = images

    payload = {
        "model": model,
        "messages": [message],
        "stream": False,
    }

    try:
        resp = requests.post(
            "http://localhost:8001/api/chat",
            json=payload,
            timeout=300
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(502, f"Ollama request failed: {e}")

    return resp.json()["message"]["content"]

