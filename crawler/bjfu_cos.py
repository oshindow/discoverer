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


def bjfu_cos():
    """爬取北林理学院教授数据模块

    利用selenimu 登录知网学者库后爬取信息
    浏览器: Google Chrome 84.0.4147.125 (请与chromedriver.exe匹配)
    目标地址：北林理学院教授主页
    不希望在调试时破坏数据库，已经注释掉了插入函数

    Author: 王心童
    """

    # 目标登陆地址
    driver = getDriver()
    url = 'http://papers.cnki.net/CAuthor/'
    driver.get(url)

    # 用户名密码登录
    login = driver.find_element_by_id(id_='link_login')
    login.click()
    username = driver.find_element_by_id(id_='username')
    username.send_keys("walston874848612@gmail.com")
    password = driver.find_element_by_id(id_='password')
    password.send_keys("wangxintong123")
    send = driver.find_element_by_id(id_='submittext')
    send.click()
    time.sleep(2)

    for i in range(0, 1):
            # 目标查询地址
            driver.get("http://expert.cnki.net/Expert/Detail/28517839.htm")
            time.sleep(6)
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

            logging.info("name:{}, page:{}".format(name, 1))

            data = tuple([name, award, school, field, domain, rank, author, title, journal, book, project, summary])
            # Insert(data)


if __name__ == '__main__':
    bjfu_cos()


