import csv
import logging
import pandas as pd
from connect import connect_page
logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )


# major是输入, 暂时记为name, 带#####<>##### 处需要将name 改为major
def readcsv():
    """ 从1.4亿中文关系数据文件中读取需要的关系数据

    Author: 刘今禹
    """
    db = connect_page()
    data = pd.read_sql("SELECT * from paperdata where trim(keywords)!=''", con=db)

    keyword = data.values[:, 5]
    name = data.values[:, 2]

    db.close()
    return name, keyword
########################################################################################################################
# 摘取所有方向
f = open('YJFX.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(["姓名", "关系", "研究方向"])
namelist = readcsv()[0]
keylist = readcsv()[1]
print("共有数据条数:", len(readcsv()[0]))
# n = 0;
# flist = []
for i in range(0, len(readcsv()[0])):
     names = namelist[i].split(";")
     keywords = keylist[i].split(";")
     for j in range(0, len(names)):
         for k in range(0, len(keywords)):
             names[j] = names[j].strip()
             keywords[k] = keywords[k].strip()
             csv_writer.writerow([names[j], "研究方向", keywords[k]])
f.close()

# datap = list(filter(None, readcsv()))  # 只能过滤空字符和None
# datap2 = ';'.join(datap)
# datap3 = datap2.split(";")
# dataf = []
# for data in datap3:
#     if data not in dataf:
#         dataf.append(data)
# print(dataf)
#

