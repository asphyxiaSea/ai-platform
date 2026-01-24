import re

    # ========== 标题正则 ==========
TITLE_RE = re.compile(
    r'(?:^|\n)\s*##\s*'
    r'([一二三四五六七八九十]+|[（(]?[一二三四五六七八九十]+[）)])'
    r'[、.\s]+([^\n]{2,30})'
)

    # ========== 1. 文本清洗 ==========
def text_filter(text: str) -> str:
    text = re.sub(r"<img[^>]*?>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</?div[^>]*?>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)  # 兜底移除其他 HTML
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

    # ========== 2. 标题归一化 ==========
def normalize_title(title: str) -> str:
        title = re.sub(r"^[一二三四五六七八九十\d]+[、\.]", "", title)
        title = re.sub(r"^[（(][一二三四五六七八九十]+[）)]", "", title)
        return title.strip()

    # ========== 3. 按全文切标题 ==========
def split_by_titles(text: str):
        sections = []
        matches = list(TITLE_RE.finditer(text))

        if not matches:
            return sections

        for i, match in enumerate(matches):
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

            prefix = match.group(1)
            title_text = match.group(2).strip()
            full_title = f"{prefix} {title_text}"

            content = text[start:end].strip()

            sections.append({
                "title": full_title,
                "content": content
            })

        return sections
def text_postprocess(
    full_text: str,
    target_sections: list[str] | None = None,
) -> str:
    """
    功能：
    1. 文本清洗（移除 img / div / HTML 标签）
    2. 提取第一页（以 \f 为分页符）
    3. 剩余全文按“大标题”切分
    4. 命中 target_sections 的章节全部保留

    参数：
    - full_text: OCR 得到的完整 markdown 文本（含 \f）
    - target_sections: 目标章节关键字列表
        如 ["项目基本情况", "项目组成员信息"]

    返回：
    - 过滤后的 markdown 文本
    """
    if not full_text:
        return ""
    
    full_text = text_filter(full_text)

    if target_sections is None:
        return full_text

    # ========== 区分第一页 ==========
    parts = full_text.split("\f", 1)
    first_page = parts[0].strip()
    rest_text = parts[1].strip() if len(parts) > 1 else ""

    kept_blocks = [first_page]

    if not rest_text or not target_sections:
        return "\n\n".join(kept_blocks)

    # ========== 全文级标题过滤 ==========
    sections = split_by_titles(rest_text)

    for sec in sections:
        title_norm = normalize_title(sec["title"])
        for target in target_sections:
            if target in title_norm:
                kept_blocks.append(
                    f"## {sec['title']}\n{sec['content'].strip()}"
                )
                break

    return "\n\n".join(kept_blocks)