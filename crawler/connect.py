import pymysql


def connect_user():
    """连接用户数据库

    Author: 王心童
    """
    db = pymysql.connect(
        host="139.219.9.206",
        user="root",
        password="Wangxintong1-",
        db="userinfo"
    )
    return db


def connect_page():
    """连接网页数据库

    Author: 王心童
    """
    db = pymysql.connect(
        host="139.219.9.206",
        user="root",
        password="Wangxintong1-",
        db="chinese"
    )
    return db


def CreateBJFU():
    """创建北林教授数据表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS bjfu")
    sql = """CREATE TABLE bjfu (
            id int PRIMARY KEY AUTO_INCREMENT,
            name CHAR(10),
            award CHAR(50), 
            school CHAR(50),
            field text, 
            domain text,
            ranking text,
            author text,
            title text,
            journal text,
            book text,
            project text,
            summary text
            )"""
    cursor.execute(sql)

    db.close()


def Insert(data):
    """插入北林教授数据库表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    sql = "INSERT INTO bjfu (name, award, school, field, domain, ranking, author, title, journal, book, project, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, data)
    db.commit()

    db.close()


def CreateCKNI():
    """创建知网搜索文章的作者数据表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS authordata")
    sql = """CREATE TABLE authordata (
            id int PRIMARY KEY AUTO_INCREMENT,
            name CHAR(255), 
            orgn CHAR(255), 
            doma CHAR(255)
            )"""
    cursor.execute(sql)

    db.close()


def Insert_paper(value):
    """插入知网搜索文章文章数据表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    sql = "INSERT INTO paperdata(title, author, journal, date, keywords, abstract) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, value)

    db.commit()
    db.close()


def Insert_author(value):
    """插入知网搜索文章作者数据表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    sql = "INSERT INTO authordata(name, orgn, doma) VALUES (%s, %s, %s)"
    cursor.execute(sql, value)

    db.commit()
    db.close()


def CreateGlobal():
    """创建全球学者数据表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS sprint1")
    sql = """CREATE TABLE sprint1 (
                id int PRIMARY KEY AUTO_INCREMENT,
                name CHAR(255),
                country CHAR(255),
                university CHAR(255),
                awards CHAR(255),
                majors CHAR(255),
                papers VARCHAR(5000),
                friends VARCHAR(5000),
                info VARCHAR(5000)
                )"""
    cursor.execute(sql)

    db.close()


def InsertGlobal(value):
    """插入全球学者数据表

    Author: 王心童
    """
    db = connect_page()
    cursor = db.cursor()

    sql = "INSERT INTO sprint1 (name, country, university, awards, majors, papers, friends, info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, value)

    db.commit()
    db.close()
