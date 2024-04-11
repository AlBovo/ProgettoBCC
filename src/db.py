from werkzeug.security import generate_password_hash
from flask import Flask, g, current_app
import mysql.connector, time

# TODO: MUST ADD ASYNC QUERIES
def addAdmin(app: Flask):
    with app.app_context():
        if 'db' not in g or not g.db.is_connected():
            getConnection(app)
        
        conn = g.db
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s)",
                        ("admin@admin.com", generate_password_hash("admin123"), True)) # TODO : admin must change the password
            conn.commit()
            cur.execute("INSERT INTO operators (id, name, surname, categories) VALUES (%s, %s, %s, %s)",
                        (1, "admin", "admin", "prova1")) # TODO : admin must change the password
            conn.commit()
        except:
            pass # admin already exists

# TODO : clear old months data

def getConnection(app: Flask):
    if 'db' not in g or not g.db.is_connected():
        while True: # wait for connection
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