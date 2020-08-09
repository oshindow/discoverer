import re
import logging
import pymysql
import pandas as pd
from flask import Flask
import sys
import csv



logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )
app = Flask(__name__)

########################################################################################################################
def read():##major是输入,暂时记为name,带#####<>#####处需要将name改为major
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="baiduyundy126",
        database="chinese"
    )
    data = pd.read_sql("SELECT * from paperdata where trim(keywords)!=''",con=db)

    keyworddd = data.values[:,5]
    nameee = data.values[:,2]

    db.close()
    return nameee,keyworddd
########################################################################################################################
    # 摘取所有方向
f = open('YJFX.csv','w',encoding='utf-8',newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(["姓名","关系","研究方向"])
namelist = read()[0]
keylist = read()[1]
print("共有数据条数:",len(read()[0]))
# n = 0;
# flist = []
for i in range(0,len(read()[0])):
     nn = namelist[i].split(";")
     kk = keylist[i].split(";")
     for j in range(0,len(nn)):
         for k in range(0,len(kk)):
             nn[j] = nn[j].strip()
             kk[k] = kk[k].strip()
             csv_writer.writerow([nn[j],"研究方向",kk[k]])
f.close()

# datap = list(filter(None, read()))  # 只能过滤空字符和None
# datap2 = ';'.join(datap)
# datap3 = datap2.split(";")
# dataf = []
# for data in datap3:
#     if data not in dataf:
#         dataf.append(data)
# print(dataf)
#

