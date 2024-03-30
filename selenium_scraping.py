from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# 初始化数据列表，用于存储爬取的数据
data = []

# Selenium浏览器设置
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10")

driver = webdriver.Chrome(options=chrome_options)

# 目标URL
url = 'https://www.dongchedi.com/auto/library/x-x-x-x-x-x-x-x-x-x-x'
driver.get(url)

try:
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待页面加载

        # 计算新的滚动高度并比较与上次滚动的高度
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # 使用BeautifulSoup解析页面
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        car_items = soup.find_all(class_='car-list_item__3nyEK')

        # 提取数据
        for item in car_items:
            series_card_name = item.find(class_='series-card_name__3QIlf')
            if series_card_name:
                href = series_card_name.get('href')
                text = series_card_name.text.strip()
                # 使用正则表达式提取ID
                match = re.search(r'/auto/series/(\d+)', href)
                if match:
                    data.append({'ID': match.group(1), '名称': text})

        # 移除重复的数据
        data = [i for n, i in enumerate(data) if i not in data[n + 1:]]
finally:
    driver.quit()  # 确保浏览器关闭

# 将数据保存到CSV文件
df = pd.DataFrame(data)
df.to_csv('car_list.csv', index=False, encoding='utf_8_sig')

print("数据已保存到CSV文件。")
