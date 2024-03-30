import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from tqdm import tqdm  # 引入进度条库

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10'
}

# 读取CSV文件获取ID列表
df_ids = pd.read_csv('car_list.csv')
ids = df_ids['ID'].unique()

# 初始化用于保存模型信息的列表
models_info = []

# 创建一个总进度条
pbar = tqdm(total=len(ids), desc="总进度", unit="ID")

# 遍历每个ID
for id in ids:
    url = f'https://www.dongchedi.com/auto/series/{id}/images-wg'
    response = requests.get(url, headers=headers)
    # 适当休眠以减少被识别为爬虫的风险
    time.sleep(1)  # 休眠1秒

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_sections = soup.find_all(class_='list_image-section__iqEH4')

        for section_index, section in enumerate(image_sections):
            car_name_tag = section.find(class_='car_car-name__2tffi')
            if car_name_tag:
                a_tag = car_name_tag.find('a')
                if a_tag:
                    model_href = a_tag['href']
                    model_name = a_tag.text.strip()
                    model_id = model_href.split('/')[-1].replace('model-', '')  # 删除model-前缀

                    # 添加模型信息到列表
                    models_info.append({'ID': id, '模型ID': model_id, '模型名称': model_name})

                    image_items = section.find_all(class_='list_image-item__1Uw4s')
                    for img_index, item in enumerate(image_items[:8]):  # 限制最多下载8张图片
                        img_tags = item.find_all('img')
                        if len(img_tags) > 1:
                            img_url = img_tags[1]['src']
                            if img_url.startswith('//'):
                                img_url = 'https:' + img_url

                            # 图片下载逻辑
                            response = requests.get(img_url, stream=True)
                            time.sleep(0.2)  # 休眠0.5秒
                            if response.status_code == 200:
                                file_path = f'images/{id}/{model_id}'
                                if not os.path.exists(file_path):
                                    os.makedirs(file_path)
                                # 构建图片文件名
                                img_name = f'{id}_{model_id}_{img_index + 1}.jpg'
                                with open(os.path.join(file_path, img_name), 'wb') as f:
                                    for chunk in response.iter_content(1024):
                                        f.write(chunk)
    pbar.update(1)  # 更新进度条

pbar.close()  # 关闭进度条

# 保存模型信息到CSV
df_models = pd.DataFrame(models_info)
df_models.to_csv('models_info.csv', index=False, encoding='utf_8_sig')
