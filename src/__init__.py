from flask_wtf import CSRFProtect
from flask import Flask
import csp, db, login
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE', 'flask')
app.secret_key = os.urandom(32).hex()
csrf = CSRFProtect()

if __name__ == '__main__':
    # add routes
    from routes import main
    app.register_blueprint(main.mainbp, url_prefix='/')
    from routes import api
    app.register_blueprint(api.apibp, url_prefix='/api')
    from routes import admin
    app.register_blueprint(admin.adminbp, url_prefix='/admin')
    
    # setup application
    csrf.init_app(app)
    csp.init_app(app)
    db.init_app(app)
    db.addAdmin(app)
    login.login_manager.init_app(app)

    app.run('0.0.0.0', port=5000, debug = True) # TODO: remove in production