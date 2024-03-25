from flask_mysqldb import MySQL, current_app
from flask import Flask

def init_app(app: Flask):
    with app.app_context():
        mysql = MySQL(app)
        cur = mysql.connection.cursor()
        cur.execute(open('db/init.sql').read())
        cur.close()

def getDatabaseCursor(app: Flask):
    mysql = MySQL(app)
    return mysql.connection.cursor()