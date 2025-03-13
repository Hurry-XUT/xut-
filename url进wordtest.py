from docx import Document
from docx.shared import Inches
import requests
from io import BytesIO

# 创建Word文档
doc = Document()

# 图片URL
image_url = 'https://example.com/path/to/image.jpg'

# 下载图片
response = requests.get(image_url)
image_bytes = BytesIO(response.content)

# 插入图片到Word文档
doc.add_picture(image_bytes, width=Inches(4.0))  # 设置图片宽度为4英寸

# 保存文档
doc.save('output.docx')
