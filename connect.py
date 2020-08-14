import pymysql
import pandas as pd


def connect_user():
    db = pymysql.connect(
        host="139.219.9.206",
        user="root",
        password="Wangxintong1-",
        db="userinfo"
    )
    return db


def connect_page():
    db = pymysql.connect(
        host="139.219.9.206",
        user="root",
        password="Wangxintong1-",
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

    db.close()

    return data


def ReadBJFU(field=None, name=None, ranking=None, domain_list=None, Peer=None, PeerRelated=None):
    db = connect_page()

    if field:

        data = pd.read_sql(
                'SELECT name, school, award, domain FROM `bjfu` where title LIKE "%s" OR field LIKE "%s";' % (field, field),
                con=db)
        name = data.values[:, 0]
        school = data.values[:, 1]
        award = data.values[:, 2]
        domain = data.values[:, 3]
        db.close()
        return name, school, award, domain

    if name and not Peer and not PeerRelated:

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
        db.close()
        return award, school, field, domain, rank, author, title, journal, book, project, summary

    if ranking and not Peer and not PeerRelated:
        name_list = pd.read_sql(
            'SELECT name FROM `bjfu` where ranking LIKE "%s" ;' % ranking,
            con=db).values[:, 0].tolist()
        db.close()
        return name_list

    if Peer:
        peer_list = pd.read_sql(
            'SELECT name FROM `bjfu` where ranking LIKE "%s"  HAVING `name` NOT LIKE "%s";' % (ranking, name),
            con=db).values[:, 0].tolist()

        return peer_list

    if PeerRelated:
        peer_data = []
        for i in range(len(domain_list)):
            data = pd.read_sql(
                'SELECT name FROM `bjfu` where domain LIKE "%s"  HAVING `name` NOT LIKE "%s";' % (
                    '%' + domain_list[i] + '%', name),
                con=db)
            peer_data.append(data.values[:, 0])

        return peer_data


def Read(name=None, school=None, major=None, multi=0):
    db = connect_page()

    if multi == 1:
        data = pd.read_sql("select name, country, university, awards, majors, papers, friends, info "
                           "from (select name, country, university, awards, majors, papers, friends, info "
                           "from sprint1 where university like '%s' )"
                           "AS F WHERE majors LIKE '%s' "
                           "ORDER By  LENGTH(trim(majors))" % (school, major), con=db)

    elif multi == 0:
        if name:
            data = pd.read_sql(
                'select name, country, university, awards, majors, papers, friends, info from sprint1 where name="%s" ' % name,
                con=db)
        elif school:
            data = pd.read_sql(
                'select name, country, university, awards, majors, papers, friends, info from sprint1 where university LIKE "%s" ' % school,
                con=db)
        elif major:
            data = pd.read_sql(
                'select name, country, university, awards, majors, papers, friends, info from sprint1 where majors LIKE "%s" ORDER By  LENGTH(trim(majors))' % major,
                con=db)

    name = data.values[:, 0]
    country = data.values[:, 1]
    school = data.values[:, 2]
    awards = data.values[:, 3]
    majors = data.values[:, 4]
    papers = data.values[:, 5]
    friends = data.values[:, 6]
    info = data.values[:, 7]

    db.close()

    return name, country, school, awards, majors, papers, friends, info


