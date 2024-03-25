from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
import os, csp, db

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE', 'flask')
app.secret_key = os.urandom(32).hex()

if __name__ == '__main__':
    # add routes
    from routes import mainbp
    app.register_blueprint(mainbp, url_prefix='/')
    from routes import apibp
    app.register_blueprint(apibp, url_prefix='/api')
    from routes import adminbp
    app.register_blueprint(adminbp, url_prefix='/admin')
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # setup application
    csp.init_app(app)
    
    # create admin user
    cur = db.getConnection(app).cursor()
    cur.execute(open('db/init.sql').read())
    cur.close()

    app.run('0.0.0.0', port=5000, debug = True) # TODO: remove in production