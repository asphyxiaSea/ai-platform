from dataclasses import dataclass

DEFAULT_SYSTEM_PROMPT = """
你是一个中文结构化信息抽取助手。
严格按照给定 Schema 输出 JSON。
不要输出 Schema 未定义的字段。
不要输出任何解释性文字。
""".strip()

@dataclass
class LLMConfig:
    model: str = "gemma3:12b"
    vl_model: str = "qwen3-vl:latest"
    temperature: float = 0.1


