from flask import Flask
from flask_mysqldb import MySQL

def getConnection(app: Flask):
    with app.app_context():
        return MySQL(app).connection