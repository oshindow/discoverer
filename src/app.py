import logging
import pymysql
import pandas as pd

from flask import Flask, render_template, request
logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )
app = Flask(__name__)


def Create_user():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        db="userinfo"
    )
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


def Insert_user(value):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        database="userinfo"
    )
    cursor = db.cursor()
    sql = "INSERT INTO userdata (email, nickname, password, institution, identity) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, value)
    db.commit()
    db.close()


def read_user(nickname=None):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        database="userinfo"
    )

    data = pd.read_sql(
            'select password from userdata where nickname="%s" ' % nickname,
            con=db)

    password = data.values[0]
    db.close()

    return password


def read(name=None, university=None, majors=None):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        database="chinese"
    )
    if name:
        data = pd.read_sql(
            'select name, country, university, awards, majors, papers, friends, info from filed_1 where name="%s" ' % name,
            con=db)
    elif university:
        data = pd.read_sql(
            'select name, country, university, awards, majors, papers, friends, info from filed_3 where university LIKE "%s" ' % university,
            con=db)
    elif majors:
        data = pd.read_sql(
            'select name, country, university, awards, majors, papers, friends, info from filed_1 where majors LIKE "%s" ' % majors,
            con=db)

    length, _ = data.values.shape
    # for i in range(0, length):
    # data = []
    # name, country, university, awards, majors, papers, friends, info = data.values[:]
    # data.append(tuple([name, country, university, awards, majors, papers, friends, info]))
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
    Create_user()
    return "用户数据库创建ok"

# 注册界面
@app.route('/register')
def register():
    return render_template("register.html")

# 登录界面
@app.route('/login')
def login():
    return render_template("login_v1.html")


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
        return render_template("register.html")

    if password == password_con:
        data = tuple([email, nickname, password, institution, identity])
        Insert_user(data)
        return render_template("temp.html")

# 登录操作
@app.route('/Login')
def Login():
    nickname = request.args.get("nickname")
    password = request.args.get("password")

    password_con = read_user(nickname)

    while password_con != password:
        return render_template("login_v1.html")

    if password_con == password:
        return render_template("temp.html")

# 搜索
@app.route('/Find_by_School')
def Find_by_School():
    university = request.args.get("school")
    university = '%' + university + '%'
    length, name, country, _, _, majors, _, _, _ = read(university=university)

    return render_template("prolist.html",
                           length=length, name=name, country=country,
                           majors=majors
                           )


@app.route('/Find_by_Major')
def Find_by_Major():
    major = request.args.get("major")
    major = '%' + major + '%'
    length, names, country, university, _, _, _, _, _ = read(majors=major)

    return render_template("prolist.html",
                           length=length, names=names.tolist(), country=country,
                           university=university
                           )


@app.route('/person')
def Find_by_Name():
    name = request.args.get("name")
    country, university, awards, majors, papers, friends, info = read(name=name)

    return render_template("person.html",
                           name=name, country=country,
                           university=university, awards=awards,
                           majors=majors, papers=papers,
                           friends=friends, info=info
                           )


if __name__ == '__main__':
    # CreateDatabasePage()
    # register()
    # Login()
    Index()
