import os
import gzip
import zipfile
import requests
from bs4 import BeautifulSoup

# 读取本地HTML文件
with open('1联系公函.html', 'r', encoding='utf-8') as f:  # 替换为实际文件名
    html_content = f.read()
# 解析HTML，提取下载链接
soup = BeautifulSoup(html_content, 'lxml')
download_tag = soup.select_one('a.LinkTxtA[href$=".zip.gz"]')  # 匹配含指定class和压缩包后缀的a标签
if download_tag:
    download_url = download_tag['href']
    print("提取到下载地址:", download_url)
    # 下载文件
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # 检查HTTP错误
        # 保存压缩包
        compressed_file = "1.zip.gz"
        with open(compressed_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"下载完成，文件已保存为: {compressed_file}")
        # 解压 .zip.gz 文件
        def extract_zip_gz(file_path):
            # 解压 .gz 文件
            with gzip.open(file_path, 'rb') as gz_file:
                # 读取解压后的内容
                decompressed_data = gz_file.read()
            # 将解压后的内容保存为 .zip 文件
            zip_file_path = file_path.replace('.gz', '')  # 去掉 .gz 后缀
            with open(zip_file_path, 'wb') as zip_file:
                zip_file.write(decompressed_data)
            # 解压 .zip 文件
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall("extracted_files")  # 解压到指定文件夹
            print(f"解压完成，文件已保存到: extracted_files")

            # 清理临时文件（可选）
            os.remove(zip_file_path)
            print("临时文件已清理")

        # 调用解压函数
        extract_zip_gz(compressed_file)

    except Exception as e:
        print("下载或解压失败:", str(e))
else:
    print("未找到符合条件的下载链接")