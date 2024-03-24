from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from . import csp
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flask')
mysql = MySQL(app)
app.secret_key = os.urandom(32).hex()

if __name__ == '__main__':
    # add routes
    from .routes import mainbp
    app.register_blueprint(mainbp, url_prefix='/')
    from .routes import apibp
    app.register_blueprint(apibp, url_prefix='/api')
    from .routes import adminbp
    app.register_blueprint(adminbp, url_prefix='/admin')
    
    # create admin user
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s)', ('admin@admin.it', os.getenv('ADMIN_PASSWORD'), True))
    cur.close()
    
    # setup application
    csp.init_app(app)
    
    app.run('0.0.0.0', port=5000, debug = True) # TODO: remove in production