from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# 配置浏览器选项
options = Options()
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 设置浏览器二进制路径

# 启动 Edge 浏览器
driver = webdriver.Edge(
    service=Service(EdgeChromiumDriverManager().install()),
    options=options
)

# 打开目标网页
url = "https://js.bysjy.com.cn/"
driver.get(url)

# 让用户手动登录
print("请手动登录并按任意键继续...")
input()

# 获取 cookies 并继续操作
cookies = driver.get_cookies()
driver.get("https://js.bysjy.com.cn/jobfair/join_company?fair_id=22051&name=%E2%80%9C%E8%81%8D%E4%BA%89%E6%9C%9D%E5%A4%95%E2%80%A2%E4%B8%8D%E8%B4%9F%E6%98%A5%E5%8D%8E%E2%80%9D2025%E5%B1%8A%E6%AF%95%E4%B8%9A%E7%94%9F%E6%98%A5%E5%AD%A3%E6%8B%9B%E8%81%98%E6%B4%BB%E5%8A%A8%EF%BC%883%E6%9C%8820%E6%97%A5%E6%9B%B2%E6%B1%9F%E6%A0%A1%E5%8C%BA%EF%BC%89")

# 设置 cookies 并刷新页面
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

# 等待页面加载
input("请手动完成页面跳转，并按任意键继续...")

# 获取当前页面内容
def get_page_content():
    return driver.page_source

# 保存 HTML
def save_page_content(page_num):
    output_file_path = f"F:\\pycharm项目\\测试\\就业办网站脚本test\\page_content_{page_num}.html"
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(get_page_content())
    print(f"第 {page_num} 页内容已保存到 {output_file_path}")

# 翻页
def go_to_next_page():
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='pane-yrz']/div/div[2]/div/button[2]"))
        )
        next_button.click()
        time.sleep(3)
    except Exception as e:
        print("翻页失败:", e)


# **开始爬取第一页**
save_page_content(1)

# **翻页并爬取后续页面**
for page_num in range(2, 4):  # 假设最多有3页
    go_to_next_page()
    save_page_content(page_num)

# 关闭浏览器
# driver.quit()

