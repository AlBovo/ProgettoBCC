from werkzeug.security import generate_password_hash
from flask import Flask, g, current_app
import mysql.connector

def addAdmin(app: Flask):
    with app.app_context():
        if 'db' not in g or not g.db.is_connected():
            getConnection(app)
        conn = g.db
        cur = conn.cursor()
        cur.execute(open('db/init.sql').read() +
                    "INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s);", 
                    ("admin@admin.com", generate_password_hash("admin"), True), multi=True)
        conn.commit()

def getConnection(app: Flask):
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host = current_app.config['MYSQL_HOST'],
            user = current_app.config['MYSQL_USER'],
            password = current_app.config['MYSQL_PASSWORD'],
            database = current_app.config['MYSQL_DB']
        )
    return g.db

def init_app(app: Flask):
    @app.teardown_appcontext
    def closeConnection(exception):
        db = g.pop('db', None)
        if db and db.is_connected():
            db.close()