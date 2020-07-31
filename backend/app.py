import re
import logging
import pymysql
import numpy as np
import pandas as pd

from lxml import etree
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from urllib.request import urlopen

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )
app = Flask(__name__)


def Create():
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
            nickname CHAR(255),
            password CHAR(255),
            university CHAR(255),
            majors CHAR(255)
            )"""
    cursor.execute(sql)
    db.close()


def Insert(value):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="090022",
        database="userinfo"
    )
    cursor = db.cursor()
    sql = "INSERT INTO userdata (nickname, password, university, majors) VALUES (%s, %s, %s, %s)"
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
    # length, _ = data.values.shape
    # for i in range(0, length):
    # data = []
    name, country, university, awards, majors, papers, friends, info = data.values
    # data.append(tuple([name, country, university, awards, majors, papers, friends, info]))

    db.close()

    return name, country, university, awards, majors, papers, friends, info

@app.route('/')
def CreateDatabasePage():
    Create()
    return "ok"

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/temp')
def temp():
    return render_template("temp.html")


@app.route('/Register')
def Register():
    nickname = request.args.get("nickname")
    password = request.args.get("password")
    password_con = request.args.get("password_con")
    university = request.args.get("university")
    majors = request.args.get("majors")

    while password_con != password:
        return render_template("register.html")

    if password == password_con:
        data = tuple([nickname, password, university, majors])
        Insert(data)
        return render_template("temp.html")


@app.route('/Login')
def Login():
    nickname = request.args.get("nickname")
    password = request.args.get("password")

    password_con = read_user(nickname)

    while password_con != password:
        return render_template("login.html")

    if password_con == password:
        return render_template("temp.html")


@app.route('/person')
def Find_by_School():
    university = request.args.get("school")
    name, country, university, awards, majors, papers, friends, info = read(university=university)

    # for i in range(0, length):
    return render_template("person.html",
                           name=name, country=country,
                           university=university, awards=awards,
                           majors=majors, papers=papers,
                           friends=friends, info=info
                           )

@app.route('/Find')
def Find():
    major = request.args.get("major")
    major = '%' + major + '%'
    name, country, university, awards, majors, papers, friends, info = read(majors=major)

    # for i in range(0, length):
    return render_template("person.html",
                           name=name, country=country,
                           university=university, awards=awards,
                           majors=majors, papers=papers,
                           friends=friends, info=info
                           )

@app.route('/person')
def Find_by_Name():
    name = request.args.get("name")
    country, university, awards, majors, papers, friends, info = read(name=name)
    
    
    # for i in range(0, length):
    return render_template("person.html",
                           name=name, country=country,
                           university=university, awards=awards,
                           majors=majors, papers=papers,
                           friends=friends, info=info
                           )


if __name__ == '__main__':
    # CreateDatabasePage()
    # register()
    Login()