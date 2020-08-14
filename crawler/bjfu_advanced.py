import time
import logging

from connect import Insert
from util import getDriver
from bs4 import BeautifulSoup
from connect import connect_page
from urllib.parse import quote

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
            )


def bjfu_advanced():
    """爬取北林教授数据高级查找模块

    利用selenimu 登录知网学者库后爬取信息
    浏览器: Google Chrome 84.0.4147.125 (请与chromedriver.exe匹配)
    目标地址：知网学者库高级查找
    可以指定任意学校与专业或是姓名
    不希望在调试时破坏数据库，已经注释掉了插入函数

    Author: 王心童
    """

    # 目标登录地址
    driver = getDriver()
    url = 'http://expert.cnki.net/Search/AdvFind'
    driver.get(url)

    # 用户名密码登录
    login = driver.find_element_by_id(id_='link_login')
    login.click()
    username = driver.find_element_by_id(id_='username')
    username.send_keys("10222726@qq.com")
    password = driver.find_element_by_id(id_='password')
    password.send_keys("wangxintong123")
    send = driver.find_element_by_id(id_='submittext')
    send.click()
    time.sleep(2)

    # 目标查询地址
    url = 'http://expert.cnki.net/Search/AdvFind'
    driver.get(url)
    unit = driver.find_element_by_name("unit_0")
    unit.send_keys("北京林业大学")
    keyword = driver.find_element_by_name("keyword_0")
    keyword.send_keys("计算机")
    btn = driver.find_element_by_class_name("mainbtn")
    btn.click()
    time.sleep(2)

    totalCnt = driver.find_element_by_id(id_='totalCnt').text
    maxpages = int(totalCnt) // 20


    count = 0
    for i in range(0, maxpages):
        url = 'http://expert.cnki.net/Search/AdvFind'
        driver.get(url)
        unit = driver.find_element_by_name("unit_0")
        unit.send_keys("北京林业大学")
        keyword = driver.find_element_by_name("keyword_0")
        keyword.send_keys("计算机")
        btn = driver.find_element_by_class_name("mainbtn")
        btn.click()
        time.sleep(2)

        # 点击下一页
        if count > 0:
            for j in range(0, count):
                driver.find_element_by_class_name('next').click()
                time.sleep(3)

        # 获取每页的10 位教授主页地址
        href = driver.find_elements_by_xpath('//*[@target="_blank"]')
        href_list = [href[3].get_attribute('href'),
                     href[6].get_attribute('href'),
                     href[9].get_attribute('href'),
                     href[12].get_attribute('href'),
                     href[15].get_attribute('href'),
                     href[18].get_attribute('href'),
                     href[21].get_attribute('href'),
                     href[24].get_attribute('href'),
                     href[27].get_attribute('href'),
                     href[30].get_attribute('href')]

        # 获取每位教授的信息
        for i in range(0, len(href_list)):

            driver.get(href_list[i])
            time.sleep(8)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            # 教授数据爬取
            name = soup.find('span', class_='nmain').text.strip('\n')
            award = soup.find('span', class_='sub').text.strip('\n')
            school = soup.find('p', class_='txt1').text.strip('\n')
            if soup.find('div', id='headResearchField'):
                field = soup.find('div', id='headResearchField').text.strip('\n')
            else:
                field = "None"

            domain = soup.find('p', id='domian-list').text.split(' ')
            domain = list(filter(None, domain))
            domain = "".join(domain).strip('\n')

            rank = soup.find('p', id='ranktitle').text.strip('\n')
            paper_list = soup.find('div', id='articlebox').text
            if soup.find('div', id='journal-list'):
                journal = soup.find('div', id='journal-list').text.strip('\n')
            else:
                journal = "None"
            if soup.find('div', id='bookBox'):
                book = soup.find('div', id='bookBox').text.strip('\n')
            else:
                book = "None"
            if soup.find('div', id='projectBox'):
                project = soup.find('div', id='projectBox').text.strip('\n')
                if project == '\n':
                    project = "None"
            else:
                project = "None"

            if soup.find('div', id='summaryBox'):
                summary = soup.find('div', id='summaryBox').text.strip('\n')
                if summary == '\n':
                    summary = "None"
            else:
                summary = "None"

            # 教授数据处理
            paper_list = paper_list.strip('\n\n').split("全文下载")
            clean_paper_list = []
            author_list = []
            for paper in paper_list:
                clean_info = paper.strip('\n\n\n').split('  ')
                allinfo = list(filter(None, clean_info))
                if len(allinfo) == 3:
                    all_author = allinfo[0]
                    all_paper = allinfo[1]
                    clean_paper_list.append(all_paper)
                else:
                    continue

                if len(all_author.split(' ')) == 2:
                    authors = all_author.split(' ')[1].strip('.').split(',')
                    for author in authors:
                        if author not in author_list:
                            author_list.append(author)

            author_list.remove(name)

            author = ";".join(author_list)
            title = ";".join(clean_paper_list)

            logging.info("name:{}, page:{}".format(name, count + 1))

            data = tuple([name, award, school, field, domain, rank, author, title, journal, book, project, summary])
            # Insert(data)

        count += 1


if __name__ == '__main__':
    bjfu_advanced()

