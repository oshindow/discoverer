import re
import logging
import pymysql
import numpy as np
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
from urllib.request import urlopen

import json

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )

'''
创建
'''
def Create():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        db="chinese"
    )
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS filed_3")
    sql = """CREATE TABLE filed_3 (
            id int PRIMARY KEY AUTO_INCREMENT,
            name CHAR(255),
            country CHAR(255),
            university CHAR(255),
            awards CHAR(255),
            majors CHAR(255),
            papers VARCHAR(10000),
            friends VARCHAR(5000),
            info VARCHAR(5000)
            )"""
    cursor.execute(sql)
    db.close()


def Insert(value):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        database="chinese"
    )
    cursor = db.cursor()
    sql = "INSERT INTO filed_3 (name, country, university, awards, majors, papers, friends, info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, value)
    db.commit()
    db.close()


if __name__ == '__main__':

    # Create()

    for i in range(1000, 1500):
        url_base = 'http://www.globalauthorid.com/WebPortal/AuthorView?wd=TZC1000'
        url = url_base + str(i)

        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        html2 = etree.HTML(url)

        name = soup.span.string
        unidata11 = soup.find('span', id='ContentPlaceHolder1_LabelRegion').get_text()
        majors = soup.find_all('span', class_='b', string=re.compile(r'学\Z'))
        info = soup.find('span', style="font-family:宋体")
        papers = soup.find_all('a', id="PMID")
        friends = soup.find_all('a', href=re.compile('\AAuthorView'))

        # 处理国籍-大学-荣誉数据 unidata11
        ##将空格替换为,
        unidata12 = unidata11.replace(" ", ",")
        # print(unidata12)
        ##网页数据分离出国家
        if len(unidata12.split(',')) >= 2:
            # print("if1读取")
            country = unidata12.split(',')[0]
            # print(country)
            unidata21 = unidata12.split(',')[1:]
            # print(unidata21)        ##21是list
            unidata22 = ",".join(unidata21)
            # print(unidata22)        ##22是未除,的str
            unidata23 = unidata22
            while (unidata23 != unidata22.strip(",")):
                unidata23 = unidata22.strip(",")
                unidata22 = unidata23
            # print(unidata23)        ##23是已除,的str，结果
            ##第一次分割，分割出country和后续字符串
            if len(unidata23.split(',')) >= 2:
                # print("if2读取")
                university = unidata23.split(',')[0]
                # print(university)
                unidata31 = unidata23.split(',')[1:]
                # print(unidata31)        ##31是list
                unidata32 = ",".join(unidata31)
                # print(unidata32)        ##32是未除,的str
                unidata33 = unidata32
                while (unidata33 != unidata32.strip(",")):
                    unidata33 = unidata32.strip(",")
                    unidata32 = unidata33
                award = unidata33
                # print(unidata33)        ##33是已除,的str，结果
            else:
                # print("if2未读取")
                university = unidata23
                award = 'None'
        else:
            # print("if1未读取")
            country = unidata12
            university = 'None'
            award = 'None'

        # 处理教授信息数据
        if info == None:
            info = 'None'
        else:
            info = info.text
        '''
        if len(university.split('  ')) == 2:
            country, uni_awa = university.split('  ')
        else:
            country = university.split(' ')[0]
            uni_awa = university.split(' ')[1:]

        uni_awa = " ".join(uni_awa)

        if len(uni_awa.split(' ')) == 2:
            university, award = uni_awa.split(' ')
        elif len(uni_awa.split(' ')) == 1:
            award = 'None'
            university = uni_awa.split(' ')
        else:
            award = 'None'
            university = "".join(uni_awa)
        '''

        major = []
        for i in majors[1:]:
            major.append(i.text)

        paper = []
        for j in papers[1:]:
            paper.append(j.text.strip('\n\r  '))

        friend = []
        for u in friends[1:]:
            friend.append(u.text)

        logging.info("name:{}".format(name))
        logging.info("country:{}".format(country))
        logging.info("university:{}".format(university))
        logging.info("award:{}".format(award))
        logging.info("major:{}".format(major))
        logging.info("paper:{}".format(paper))
        logging.info("friend:{}".format(friend))
        logging.info("info:{}".format(info))

        data = tuple([name, country, university, award, " ".join(major), " ".join(paper), " ".join(friend), info])
        Insert(data)


    '''
    with open('D:\\s729\\test.json', 'w') as file:
        file.write(str(name))
        file.write(str(University))
        file.write(str(Direction))
        file.write(str(Works))
    '''