#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

def read(name):
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        password="baiduyundy126",
        database="chinese",
        charset='utf8'
    )
    ##name是输入值
    cursor = db.cursor()
    '''
    name (str)
    
    '''
    am = name
    s = list(am)
    am = '%' + '%'.join(s) + '%'
    # SQL 查询语句
    sql = "SELECT * FROM filed_3 WHERE majors like '%s'" % am
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    listn = []
    for row in results:
        list1 = listn
        list2 = [row[1]]
        listn = list1 + list2
    db.close()
    return listn


print(read("临床医学"))