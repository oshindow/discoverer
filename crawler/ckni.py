import re
import time
import logging

from util import util
from bs4 import BeautifulSoup
from connect import Insert_paper, Insert_author
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )


def scraping(driver, field):
    """ 按研究领域抓取知网论文数据与作者数据模块

    :param driver: selenium.webdriver.Chrome()
    浏览器: Google Chrome 84.0.4147.125 (请与chromedriver.exe匹配)
    :param field: 研究领域关键词
    不希望在调试时破坏数据库，已经注释掉了插入函数

    Author: 王心童
    """
    try:
        # 输入研究领域关键词
        FindField = driver.find_element_by_id(id_='txt_1_value1')
        FindField.send_keys(field)

        FindField.send_keys(Keys.ENTER)

    except NoSuchElementException:
        print('element cannot be found!')
    time.sleep(5)

    # 切换至frameResult
    driver.switch_to_frame('iframeResult')
    # 获取结果记录条数
    # TODO 这里总抛异常NoSuchElementException，应改用显式等待
    try:
        res_number = str(driver.find_element_by_css_selector('div.pagerTitleCell').text.split(' ')[2])
        res_number = int("".join(res_number.split(',')))
    except NoSuchElementException:
        print('页面解析出错，准备进行重试')
        time.sleep(3)
        res_number = str(driver.find_element_by_css_selector('div.pagerTitleCell').text.split(' ')[2])
        res_number = int("".join(res_number.split(',')))

    print('开始抓取【' + field + '】的论文信息，共找到【' + str(res_number) + '】条记录')
    if res_number <= 20:
        # 结果数量不足20条，只有一页
        # 抓取结果列表
        tbody = driver.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody')
        # 点击所有的“显示全部作者”按钮
        showAlls = tbody.find_elements_by_class_name('showAll')
        for e in showAlls:
            e.click()
        # 遍历结果的每条记录(标题、作者、期刊、时间)
        trs = tbody.find_elements_by_tag_name('tr')
        paper = driver.find_elements_by_class_name('fz14')

        for j in range(0, len(paper)):
            tds = trs[j + 1].find_elements_by_tag_name('td')
            # 存放每一条结果记录
            title = tds[1].text
            author = tds[2].text
            journal = tds[3].text
            date = tds[4].text

            logging.info("title:{}".format(title))
            logging.info("author:{}".format(author))
            logging.info("journal:{}".format(journal))
            logging.info("date:{}".format(date))

            # 找到论文主页的链接
            href = paper[j].get_attribute('href')
            pattern = re.compile(r'(?:URLID=)(.*)&')
            URLID = pattern.findall(href)[0]
            href = 'https://kns.cnki.net/KCMS/detail/' + URLID + '.html'
            href = urlopen(href).read().decode('utf-8')
            soup = BeautifulSoup(href, 'lxml')

            # 找到论文的关键词、摘要
            keyword = soup.find('label', id='catalog_KEYWORD')
            abstract = soup.find('label', id='catalog_ABSTRACT')

            if abstract:
                abstract = "".join(abstract.parent.text.split('：')[1:]).strip()
            else:
                abstract = 'None'
            if keyword:
                keyword = "".join(keyword.parent.text.split('：')[1:]).strip()
                keyword = keyword.strip(';').split(';\r\n')
                keywords = []
                for i in range(0, len(keyword)):
                    keywords.append(keyword[i].strip())
                keywords = ";".join(keywords)
            else:
                keywords = None

            logging.info("abstract:{}".format(abstract))
            logging.info("keywords:{}".format(keywords))

            paper_data = tuple([title, author, journal, date, keywords, abstract])
            # Insert_paper(paper_data)

        # 找到作者的主页
        popul = driver.find_elements_by_class_name('KnowledgeNetLink')
        for k in range(0, len(popul)):
            href = popul[k].get_attribute('href')
            href = urlopen(href).read().decode('utf-8')
            soup = BeautifulSoup(href, 'lxml')

            doma = soup.find('p', class_='doma')
            name = soup.find('h2', class_='name')
            orgn = soup.find('p', class_='orgn')

            if doma:
                doma = doma.text
            else:
                doma = 'None'
            if name:
                name = name.text
            else:
                name = 'None'
            if orgn:
                orgn = orgn.text
            else:
                orgn = 'None'

            logging.info("doma:{}".format(doma))
            logging.info("name:{}".format(name))
            logging.info("orgn:{}".format(orgn))

            author_data = tuple([name, orgn, doma])
            # Insert_author(author_data)
    else:
        # 结果数量超过20条，不止一页
        # 获取最大页数
        max_page = int(
            driver.find_element_by_css_selector('div.TitleLeftCell').find_elements_by_tag_name('a')[-2].text)
        for i in range(1, max_page + 1):
            print('开始抓取第' + str(i) + '页')

            # 找到论文的主页
            # 找到论文的标题
            tbody = driver.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody')
            # 点击所有的“显示全部作者”按钮
            showAlls = tbody.find_elements_by_class_name('showAll')
            for e in showAlls:
                e.click()
            # 遍历结果的每条记录(标题、作者、期刊、时间)
            trs = tbody.find_elements_by_tag_name('tr')
            paper = driver.find_elements_by_class_name('fz14')

            for j in range(0, len(paper)):
                tds = trs[j + 1].find_elements_by_tag_name('td')
                # 存放每一条结果记录
                title = tds[1].text
                author = tds[2].text
                journal = tds[3].text
                date = tds[4].text

                logging.info("title:{}".format(title))
                logging.info("author:{}".format(author))
                logging.info("journal:{}".format(journal))
                logging.info("date:{}".format(date))

                # 找到论文主页的链接
                href = paper[j].get_attribute('href')
                pattern = re.compile(r'(?:URLID=)(.*)&')
                URLID = pattern.findall(href)[0]
                href = 'https://kns.cnki.net/KCMS/detail/' + URLID + '.html'
                href = urlopen(href).read().decode('utf-8')
                soup = BeautifulSoup(href, 'lxml')

                # 找到论文的关键词、摘要
                keyword = soup.find('label', id='catalog_KEYWORD')
                abstract = soup.find('label', id='catalog_ABSTRACT')

                if abstract:
                    abstract = "".join(abstract.parent.text.split('：')[1:]).strip()
                else:
                    abstract = 'None'
                if keyword:
                    keyword = "".join(keyword.parent.text.split('：')[1:]).strip()
                    keyword = keyword.strip(';').split(';\r\n')
                    keywords = []
                    for i in range(0, len(keyword)):
                        keywords.append(keyword[i].strip())
                    keywords = ";".join(keywords)
                else:
                    keywords = None

                logging.info("abstract:{}".format(abstract))
                logging.info("keywords:{}".format(keywords))

                paper_data = tuple([title, author, journal, date, keywords, abstract])
                # Insert_paper(paper_data)

            # 找到作者的主页
            popul = driver.find_elements_by_class_name('KnowledgeNetLink')
            for k in range(0, len(popul)):
                href = popul[k].get_attribute('href')
                href = urlopen(href).read().decode('utf-8')
                soup = BeautifulSoup(href, 'lxml')

                doma = soup.find('p', class_='doma')
                name = soup.find('h2', class_='name')
                orgn = soup.find('p', class_='orgn')

                if doma:
                    doma = doma.text
                else:
                    doma = 'None'
                if name:
                    name = name.text
                else:
                    name = 'None'
                if orgn:
                    orgn = orgn.text
                else:
                    orgn = 'None'

                logging.info("doma:{}".format(doma))
                logging.info("name:{}".format(name))
                logging.info("orgn:{}".format(orgn))

                author_data = tuple([name, orgn, doma])
                # Insert_author(author_data)

            # 点击下一页按钮
            if i != max_page:
                next_page = driver.find_element_by_css_selector('div.TitleLeftCell').find_elements_by_tag_name('a')[
                    -1]
                next_page.click()

    logging.info('{}的所有论文信息抓取完毕'.format(field))


if __name__ == '__main__':
    driver = util.getDriver()
    fields = ['人工智能', "指纹识别", "声纹识别", "词向量", "建模", "聊天机器人", "语音唤醒", "可视化"]

    for field in fields:
        time.sleep(1)
        scraping(driver=driver, field=field)

    driver.quit()