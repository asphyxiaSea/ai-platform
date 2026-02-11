from functools import lru_cache
from pathlib import Path
import re


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fa5]", "", text)
    return text


@lru_cache(maxsize=1)
def _load_sensitive_words() -> list[str]:
    base_dir = Path(__file__).resolve().parents[2]
    sensitive_dir = base_dir / "assets" / "sensitive_words_files"
    words: list[str] = []

    if not sensitive_dir.exists():
        return words

    for path in sensitive_dir.iterdir():
        if not path.is_file() or path.suffix != ".txt":
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    words.append(word)
    return words


def filter_sensitive_text(text: str) -> str:
    sensitive_words = _load_sensitive_words()
    replaced_text = text
    norm_text = _normalize(text)

    for word in sensitive_words:
        if word in replaced_text or word in norm_text:
            replaced_text = replaced_text.replace(word, "*" * len(word))

    return replaced_text
