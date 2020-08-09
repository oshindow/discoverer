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


def Create():
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


if __name__ == '__main__':
    Create()

'''
def Create():
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
'''
