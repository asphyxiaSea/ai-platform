import os
import re


def normalize(text: str):
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fa5]", "", text)
    return text


def load_sensitive_words_from_dir(dir_path: str) -> list[str]:
    sensitive_words = []

    for filename in os.listdir(dir_path):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(dir_path, filename)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    sensitive_words.append(word)

    return sensitive_words


def main():
    # 1️⃣ 从本地文件夹加载敏感词
    sensitive_dir = "assets/sensitive_words_files"
    sensitive_words = load_sensitive_words_from_dir(sensitive_dir)

    # 2️⃣ 测试文本
    text = "这是一个测试文本，包含敏感词：习近平。"

    replaced_text = text
    norm_text = normalize(text)

    # 3️⃣ 执行替换
    for w in sensitive_words:
        if w in replaced_text or w in norm_text:
            replaced_text = replaced_text.replace(w, "*" * len(w))

    return {
        "result": replaced_text
    }


if __name__ == "__main__":
    result = main()
    print(result)
