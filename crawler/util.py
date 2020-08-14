import os
from selenium import webdriver


def getDriver():
    """ selenium 获取浏览器对象

    浏览器: Google Chrome 84.0.4147.125 (请与chromedriver.exe匹配)

    Author: 王心童
    """
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=' + UserAgent)
    executable_path = os.getcwd() + os.sep + 'chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path,
                              chrome_options=options)
    return driver




