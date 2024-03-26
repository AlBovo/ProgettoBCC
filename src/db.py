from werkzeug.security import generate_password_hash
from flask import Flask, g, current_app
import mysql.connector, time

def addAdmin(app: Flask):
    with app.app_context():
        if 'db' not in g or not g.db.is_connected():
            getConnection(app)
        
        conn = g.db
        cur = conn.cursor()
        
        for i in open('db/init.sql').read().split('-- SPLIT'):
            cur.execute(i)
            conn.commit()
        try:
            cur.execute("INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s)",
                        ("admin@admin.com", generate_password_hash("admin"), True))
            conn.commit()
        except:
            pass # admin already exists

def getConnection(app: Flask):
    if 'db' not in g or not g.db.is_connected():
        while True: # TODO : find a better way to do this
            try:
                g.db = mysql.connector.connect(
                    host = current_app.config['MYSQL_HOST'],
                    user = current_app.config['MYSQL_USER'],
                    password = current_app.config['MYSQL_PASSWORD'],
                    database = current_app.config['MYSQL_DB']
                )
                break
            except:
                time.sleep(1)
    return g.db

def init_app(app: Flask):
    @app.teardown_appcontext
    def closeConnection(exception):
        db = g.pop('db', None)
        if db and db.is_connected():
            db.close()