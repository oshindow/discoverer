import pymysql


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