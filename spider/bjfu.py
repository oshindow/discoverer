import time
import logging

from util import util
from bs4 import BeautifulSoup
from connect import connect_page
from urllib.parse import quote

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
            )


def Insert(data):
    db = connect_page()
    cursor = db.cursor()

    sql = "INSERT INTO bjfu (name, award, school, field, domain, ranking, author, title, journal, book, project, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, data)
    db.commit()

    db.close()


if __name__ == '__main__':

    driver = util.getDriver()

    url = 'http://papers.cnki.net/CAuthor/'
    driver.get(url)

    login = driver.find_element_by_id(id_='link_login')
    login.click()
    username = driver.find_element_by_id(id_='username')
    username.send_keys("18600503086")
    password = driver.find_element_by_id(id_='password')
    password.send_keys("baiduyundy126")
    send = driver.find_element_by_id(id_='submittext')
    send.click()
    time.sleep(2)

    url = 'http://papers.cnki.net/CAuthor/Search/Find?q=' + quote('北京林业大学') + '&type=1'
    driver.get(url)
    totalCnt = driver.find_element_by_id(id_='totalCnt').text
    maxpages = int(totalCnt) // 20
    count = 48
    for i in range(0, maxpages):
        url = 'http://papers.cnki.net/CAuthor/Search/Find?q=' + quote('北京林业大学') + '&type=1'
        driver.get(url)
        if count > 0:
            for j in range(0, count):
                driver.find_element_by_class_name('next').click()
                time.sleep(3)
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

        for i in range(0, len(href_list)):

            driver.get(href_list[i])
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
                clean_paper = paper.strip('\n\n\n').split('\n')[0].split(' ')

                allinfo = list(filter(None, clean_paper))
                if len(allinfo) == 3:
                    _, author, title = allinfo
                    single_author = author.strip('.').split(',')
                    for p in single_author:
                        author_list.append(p)
                    clean_paper_list.append(title)
                else:
                    continue

            authors = []
            for author in author_list:
                if author not in authors:
                    authors.append(author)
            authors.remove(name)

            author = ";".join(authors)
            title = ";".join(clean_paper_list)

            logging.info("name:{}, page:{}".format(name, count + 1))

            data = tuple([name, award, school, field, domain, rank, author, title, journal, book, project, summary])
            Insert(data)

        count += 1


