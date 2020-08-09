import os
import random
import re

import openpyxl
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def get_field_list():
    # 直接从内存中获取名单列表
    authors = [
        "指纹识别", "声纹识别", "词向量", "建模", "聊天机器人", "语音唤醒", "可视化"
    ]
    return authors


def getDriver():
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=' + UserAgent)
    executable_path = os.getcwd() + os.sep + 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path,
                              chrome_options=options)
    return driver




