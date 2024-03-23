from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import jwt, uuid, os

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') | 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER') | 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') | 'root'
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') | 'flask'
mysql = MySQL(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug = True) # TODO: remove in production