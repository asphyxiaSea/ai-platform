from dataclasses import dataclass


@dataclass
class PaddleConfig:
    pipeline: str = "default"
