from marker.output import text_from_rendered
from util.mark_pdf import CONVERTER
from io import BytesIO

pdf_path = "assets/桉树人工林土壤质量演变与提升关键技术——获奖个人证书.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

pdf_stream = BytesIO(pdf_bytes)


# 3. 初始化转换器
# 你可以在这里指定语言

# 4. 执行转换
rendered = CONVERTER(pdf_stream)

# 5. 提取文本内容
full_text, _, _ = text_from_rendered(rendered)

print(full_text)

