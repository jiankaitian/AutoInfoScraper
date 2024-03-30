# 懂车帝汽车信息爬取项目

## 项目概述

本项目旨在从懂车帝网站（https://www.dongchedi.com）爬取汽车系列及其模型的信息和相关图片。项目分为两大部分：首先使用Selenium和BeautifulSoup库爬取汽车系列的基本信息，并将这些信息保存到CSV文件中；然后，通过requests和BeautifulSoup库对每个汽车系列的模型进行深入爬取，获取模型的详细信息和图片，最终将图片保存到本地，并将模型信息存储到另一个CSV文件中。

## 环境依赖

本项目依赖以下Python库：

- selenium
- beautifulsoup4
- pandas
- requests
- tqdm

请确保安装了Chrome浏览器和对应版本的ChromeDriver，并将ChromeDriver的路径添加到系统环境变量中。

## 使用方法

### 第一部分：爬取汽车系列信息

1. 确保已经设置好Selenium环境，包括安装ChromeDriver。
2. 运行第一部分的代码，此代码将自动打开懂车帝网站，通过模拟浏览器滚动来加载全部汽车系列的信息，然后提取并保存这些信息到`car_list.csv`文件中。

### 第二部分：爬取汽车模型信息及图片

1. 在成功执行第一部分代码并生成`car_list.csv`文件后，运行第二部分的代码。
2. 代码将读取`car_list.csv`中的汽车系列ID，对每个ID进行遍历，访问相应的URL来爬取每个系列下的汽车模型信息和图片。
3. 每个模型的图片将被保存到`images/{系列ID}/{模型ID}`目录下，模型信息将被保存到`models_info.csv`文件中。

## 注意事项

- 请在合法范围内使用此爬虫项目，遵守《懂车帝》网站的爬虫政策和相关法律法规。
- 为避免给目标网站服务器带来不必要的负担，建议在爬取数据时适当增加等待时间。

## 代码结构

本项目包括以下主要文件和目录：

```
懂车帝汽车信息爬取项目/
│
├── car_list.csv - 存储从懂车帝网站爬取的汽车系列信息。
├── models_info.csv - 存储从懂车帝网站爬取的汽车模型信息。
│
├── images/ - 该目录下包含所有下载的汽车模型图片，按系列ID和模型ID组织。
│   ├── {系列ID}/
│   │   ├── {模型ID}/
│   │   │   ├── {系列ID}_{模型ID}_{图片编号}.jpg
│   │   │   └── ...
│   │   └── ...
│   └── ...
│
├── selenium_scraping.py - 使用Selenium和BeautifulSoup爬取汽车系列的脚本。
│
└── requests_scraping.py - 使用requests和BeautifulSoup爬取汽车模型信息及图片的脚本。
```

### selenium_scraping.py

此脚本负责第一部分的爬取工作，主要步骤如下：

1. 使用Selenium打开懂车帝网站，通过模拟浏览器滚动加载全部汽车系列的信息。
2. 使用BeautifulSoup解析页面内容，提取汽车系列的ID和名称，并保存到`car_list.csv`文件中。

### requests_scraping.py

此脚本负责第二部分的爬取工作，主要步骤如下：

1.

 读取`car_list.csv`文件，获取所有汽车系列的ID。
2. 对每个系列ID，构建对应的URL，使用requests访问并使用BeautifulSoup解析页面。
3. 提取每个系列下的汽车模型信息和图片URL，并下载图片到本地`images/`目录下。
4. 保存所有模型的信息到`models_info.csv`文件中。

## 运行项目

1. 确保已安装所有依赖库。
2. 首先运行`selenium_scraping.py`脚本来爬取并生成`car_list.csv`文件。
3. 然后运行`requests_scraping.py`脚本，该脚本会读取`car_list.csv`中的数据，爬取各汽车模型的详细信息和图片，保存到`models_info.csv`和`images/`目录。
