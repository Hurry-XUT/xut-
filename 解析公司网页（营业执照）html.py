import os
import re

import requests
from bs4 import BeautifulSoup
from docx import Document
from lxml import etree
base_folder = r"F:\pycharm项目\测试\就业办网站脚本test\3.26双选"
for i in range(1,31):
    with open(f"{i}.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    tree = etree.HTML(html_content)
    name_elements = tree.xpath('//*[@id="app"]/div[1]/div[1]/div/div/div[2]/div/p')
    if name_elements:
        name = name_elements[0].text.strip()  # 提取第一个 <p> 标签的文本并去除空白字符
    else:
        name = "未知公司"
    photo_img = tree.xpath('//*[@id="pane-base"]/div[10]/div/div[2]/div/div/img')
    if photo_img:
        img_url = photo_img[0].get("src")
        print(f"公司名称: {name}")
        print(f"特定图片 URL: {img_url}")

        # 创建公司文件夹
        company_folder = os.path.join(base_folder, name)
        os.makedirs(company_folder, exist_ok=True)

        # 下载图片
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # 检查请求是否成功

            # 生成图片保存路径
            img_extension = os.path.splitext(img_url)[1]  # 获取文件扩展名（如 .jpg, .png）
            img_name = f"{name}-营业执照{img_extension}"  # 新文件名：公司名-营业执照.扩展名
            save_path = os.path.join(company_folder, img_name)

            # 保存图片
            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"图片已保存到: {save_path}")
        except Exception as e:
            print(f"下载失败: {e}")
    else:
        print(f"未找到符合条件的图片（文件: {i}.html）")

