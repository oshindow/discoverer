import logging
import pandas as pd

from connect import connect_page, connect_user
from flask import Flask, render_template, request

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )
app = Flask(__name__)


def CreateUser():
    db = connect_user()
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS userdata")
    sql = """CREATE TABLE userdata (
            id int PRIMARY KEY AUTO_INCREMENT,
            email CHAR(255),
            nickname CHAR(255),
            password CHAR(255),
            institution CHAR(255),
            identity CHAR(255)
            )"""
    cursor.execute(sql)

    db.close()


def InsertUser(data):
    db = connect_user()
    cursor = db.cursor()

    sql = "INSERT INTO userdata (email, nickname, password, institution, identity) VALUES (%s, %s, %s, %s, %s)"

    cursor.execute(sql, data)
    db.commit()

    db.close()


def ReadUser(email):
    db = connect_user()

    data = pd.read_sql(
            'select password from userdata where email="%s" ' % email,
            con=db)

    password = data.values[0]
    db.close()

    return password


def Read(name=None, university=None, majors=None):
    db = connect_page()

    if name:
        data = pd.read_sql(
            'select name, country, university, awards, majors, papers, friends, info from sprint1 where name="%s" ' % name,
            con=db)
    elif university:
        data = pd.read_sql(
            'select name, country, university, awards, majors, papers, friends, info from sprint1 where university LIKE "%s" ' % university,
            con=db)
    elif majors:
        data = pd.read_sql(
            'select name, country, university, awards, majors, papers, friends, info from sprint1 where majors LIKE "%s" ' % majors,
            con=db)

    length, _ = data.values.shape

    name = data.values[:, 0]
    country = data.values[:, 1]
    university = data.values[:, 2]
    awards = data.values[:, 3]
    majors = data.values[:, 4]
    papers = data.values[:, 5]
    friends = data.values[:, 6]
    info = data.values[:, 7]

    db.close()

    return length, name, country, university, awards, majors, papers, friends, info


@app.route('/')
def CreateDatabasePage():
    CreateUser()
    return "用户数据库创建ok"

# 登录 & 注册界面
@app.route('/login')
def login():
    return render_template("login.html")

# 网站主页
@app.route('/index')
def Index():
    return render_template("index.html")

# 注册操作
@app.route('/Register')
def Register():
    email = request.args.get("email")
    nickname = request.args.get("nickname")
    password = request.args.get("password")
    password_con = request.args.get("password_con")
    institution = request.args.get("institution")
    identity = request.args.get("identity")

    while password_con != password:
        return render_template("login.html")

    if password == password_con:
        data = tuple([email, nickname, password, institution, identity])
        InsertUser(data)
        return render_template("index.html")

# 登录操作
@app.route('/Login')
def Login():
    email = request.args.get("email")
    password = request.args.get("password")

    password_con = ReadUser(email)

    while password_con != password:
        return render_template("login.html")

    if password_con == password:
        return render_template("index.html")

# 搜索
@app.route('/Find_by_School')
def Find_by_School():
    university = request.args.get("fname")
    university = '%' + university + '%'

    length, names, country, university, awards, majors, _, _, _ = Read(university=university)

    return render_template("searchprolist.html",
                           length=length, names=names, country=country,
                           university=university,
                           majors=majors)


@app.route('/Find_by_Major')
def Find_by_Major():
    major = request.args.get("fname")
    major = '%' + major + '%'

    length, names, country, university, awards, majors, _, _, _, = Read(majors=major)

    return render_template("searchprolist.html",
                           length=length, names=names, country=country,
                           university=university,
                           majors=majors)


@app.route('/Find_by_Name')
def Find_by_Name():
    name = request.args.get("fname")
    length, name, country, university, awards, majors, papers, friends, info = Read(name=name)

    papers = papers[0].split(';')
    friends = friends[0].split(';')
    majors = majors[0].split(';')

    return render_template("person.html",
                           name=" ".join(name), country=" ".join(country),
                           university=" ".join(university), awards=" ".join(awards),
                           majors=majors, papers=papers,
                           friends=friends, info=info
                           )


'''
@app.route('/index')
def Find():

    idmajor = request.args.get("major")
    idschool = request.args.get("school")
    idname = request.args.get("name")

    logging.info("idmajor:{}".format(idmajor))
    logging.info("idschool:{}".format(idschool))
    logging.info("idname:{}".format(idname))

    if idmajor == "专业":
        Find_by_Major()
    elif idmajor == "学校":
        Find_by_School()
    elif idmajor == "姓名":
        Find_by_Name()
'''

if __name__ == '__main__':
    # CreateDatabasePage()
    app.run()

