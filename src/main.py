from flask import Blueprint, Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flask')
mysql = MySQL(app)
app.secret_key = os.urandom(32).hex()

# TODO : add blueprints registration

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug = True) # TODO: remove in production