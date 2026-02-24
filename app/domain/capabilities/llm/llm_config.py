from dataclasses import dataclass

@dataclass
class LLMConfig:
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"
    temperature: float = 0.1


