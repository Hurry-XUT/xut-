import os
import gzip
import zipfile
import re
import os

from bs4 import BeautifulSoup
import requests

def sanitize_company_name(name):
    """清理公司名称中的非法字符"""
    clean_name = re.sub(r'[\\/:*?"<>|]', '', name).strip()
    return clean_name if clean_name else "未知公司"


def process_contact_letter(i, company_name, company_folder):
    # 解析HTML获取下载链接
    with open(f'{i}联系公函.html', "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    download_tag = soup.select_one('a.LinkTxtA[href$=".zip.gz"]')
    if not download_tag:
        print(f"[错误] 未找到压缩包链接（文件: {i}联系公函.html）")
        return
    # 处理URL
    relative_url = download_tag['href']
    # 下载压缩包
    try:
        response = requests.get(relative_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[错误] 下载失败: {relative_url} - {str(e)}")
        return

    # 创建临时目录处理压缩包
    with tempfile.TemporaryDirectory() as temp_dir:
        # 保存压缩包
        zip_gz_path = os.path.join(temp_dir, "temp.zip.gz")
        with open(zip_gz_path, 'wb') as f:
            f.write(response.content)
        try:
            # 解压.gz -> .zip
            zip_path = os.path.join(temp_dir, "temp.zip")
            with gzip.open(zip_gz_path, 'rb') as f_in:
                with open(zip_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # 解压ZIP文件
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            # 查找有效文件
            valid_ext = ('.pdf', '.jpg', '.jpeg', '.png')
            extracted_files = []
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(valid_ext):
                        extracted_files.append(os.path.join(root, file))
            if not extracted_files:
                print(f"[警告] 未找到PDF/图片文件（文件: {i}联系公函.html）")
                return

            # 保存到公司目录
            for src_path in extracted_files:
                # 生成目标文件名
                ext = os.path.splitext(src_path)[1]
                dest_name = f"{name}-联系公函{ext}"
                dest_path = os.path.join(company_folder, dest_name)

                # 处理重复文件
                counter = 1
                while os.path.exists(dest_path):
                    dest_name = f"{company_name}-联系公函({counter}){ext}"
                    dest_path = os.path.join(company_folder, dest_name)
                    counter += 1

                shutil.copy(src_path, dest_path)
                print(f"[成功] 保存联系公函文件: {os.path.basename(dest_path)}")

        except (gzip.BadGzipFile, zipfile.BadZipFile) as e:
            print(f"[错误] 压缩包损坏: {e}")
        except Exception as e:
            print(f"[错误] 解压过程异常: {e}")