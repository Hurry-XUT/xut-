from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import time
import requests
from bs4 import BeautifulSoup
def go_to_next_page():
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='pane-yrz']/div/div[2]/div/button[2]"))
        )
        next_button.click()
        print("翻页成功！")
        time.sleep(3)
    except Exception as e:
        print("翻页失败:", e)
print("启动！")
# 配置浏览器选项
options = Options()
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 设置浏览器二进制路径
print("正在准备启动浏览器！")
# 启动 Edge 浏览器
driver = webdriver.Edge(
    service=Service(EdgeChromiumDriverManager().install()),
    options=options
)
driver.maximize_window()
print("继续启动！")
# 打开目标网页
url = "https://js.bysjy.com.cn/"
driver.get(url)
button_login = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[1]/div[1]").click()
button_account = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/input")
button_account.send_keys("助理账号")
print("输入账号成功")
button_password = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div[1]/div[3]/div[1]/div[2]/input")
button_password.send_keys("助理账号密码")
print("输入密码成功")
# 让用户手动登录
print("请手动输入验证码并按任意键继续...")
input()
# 获取 cookies 并继续操作
cookies = driver.get_cookies()
driver.get("https://js.bysjy.com.cn/jobfair/join_company?fair_id=22049&name=%E2%80%9C%E8%81%8C%E4%BA%89%E6%9C%9D%E5%A4%95%E2%80%A2%E4%B8%8D%E8%B4%9F%E6%98%A5%E5%8D%8E%E2%80%9D2025%E5%B1%8A%E6%AF%95%E4%B8%9A%E7%94%9F%E6%98%A5%E5%AD%A3%E6%8B%9B%E8%81%98%E6%B4%BB%E5%8A%A8%EF%BC%883%E6%9C%8826%E6%97%A5%E9%87%91%E8%8A%B1%E6%A0%A1%E5%8C%BA%EF%BC%89")
# 设置 cookies 并刷新页面
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
# 等待页面加载
input("请手动完成页面跳转，并按任意键继续...")
button1 = driver.find_element(By.XPATH,"/html/body/section/section/main/div[1]/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]").click()
print("成功点击审核状态")
time.sleep(2)
print("请手动点击待审核")
time.sleep(5)
print("点击待审核成功")
for j in range(0,4):
    original_window = driver.current_window_handle  # 保存原窗口句柄
    for i in range(1, 11):
        time.sleep(1)
        try:
            # 步骤1：显式等待元素存在（最多等待10秒）
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"/html/body/section/section/main/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[{i}]/td[4]/div/div[2]/span/div")  # 替换为你的元素定位
                )
            )

            # 步骤2：通过JavaScript直接触发点击
            driver.execute_script("arguments[0].click();", element)

            print("点击成功！")

        except Exception as e:
            print(f"操作失败：{e}")

        # 获取所有窗口句柄，新窗口通常是最后一个
        all_windows = driver.window_handles
        new_window = [window for window in all_windows if window != original_window][0]

        # 切换到新窗口
        driver.switch_to.window(new_window)
        time.sleep(1)
        # print("点击基本信息")
        # try:
        #     # 步骤1：显式等待元素存在（最多等待10秒）
        #     element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located(
        #             (By.XPATH, "/html/body/section/section/main/div[1]/div[1]/div[3]/div[1]/div/div/div/div[2]")  # 替换为你的元素定位
        #         )
        #     )
        #
        #     # 步骤2：通过JavaScript直接触发点击
        #     driver.execute_script("arguments[0].click();", element)
        #
        #     print("点击成功！")
        #
        # except Exception as e:
        #     print(f"操作失败：{e}")
        # 获取 HTML 内容
        time.sleep(1)
        html_content = driver.page_source

        # 保存到文件
        with open(f"招聘简章{10*j+i}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # driver.quit()
        driver.close()
        driver.switch_to.window(original_window)
    go_to_next_page()
    time.sleep(2)
time.sleep(5)