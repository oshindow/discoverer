import pymysql
import pandas as pd

def connect_user():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        db="userinfo"
    )
    return db


def connect_page():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        db="chinese"
    )
    return db


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

def ReadPaper(field=None, name=None):
    db = connect_page()
    if field:
        data = pd.read_sql(
                'SELECT name, school, award, domain FROM `bjfu` where title LIKE "%s" OR field LIKE "%s";' % (field, field),
                con=db)
        name = data.values[:, 0]
        school = data.values[:, 1]
        award = data.values[:, 2]
        domain = data.values[:, 3]
        return name, school, award, domain

    if name:

        data = pd.read_sql(
            'SELECT award, school, field, domain, ranking, author, title, journal, book, project, summary '
            'FROM `bjfu` where name="%s"' % (name),
            con=db)

        award = data.values[0][0]
        school = data.values[0][1]
        field = data.values[0][2]
        domain = data.values[0][3]
        rank = data.values[0][4]
        author = data.values[0][5]
        title = data.values[0][6]
        journal = data.values[0][7]

        if data.values[0][8]:
            book = data.values[0][8]
        else:
            book = " "
        if data.values[0][9]:
            project = data.values[0][9]
        else:
            project = " "
        if data.values[0][10]:
            summary = data.values[0][10]
        else:
            summary = " "

        return award, school, field, domain, rank, author, title, journal, book, project, summary


def Read(name=None, university=None, majors=None, multi=0):
    db = connect_page()

    if multi == 1:
        data = pd.read_sql("select name, country, university, awards, majors, papers, friends, info FROM (select name, country, university, awards, majors, papers, friends, info from sprint1 where university like '%s' )AS F WHERE majors LIKE '%s' ORDER By  LENGTH(trim(majors))" % (university, majors), con=db)

    elif multi == 0:
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
                'select name, country, university, awards, majors, papers, friends, info from sprint1 where majors LIKE "%s" ORDER By  LENGTH(trim(majors))' % majors,
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


