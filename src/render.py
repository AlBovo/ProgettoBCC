from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['FRONTEND'] = True
app.config['SECRET_KEY'] = 'gasighoagohsaighaoigshaisgh'
csrf = CSRFProtect(app)
api = Blueprint('api', __name__)
main = Blueprint('main', __name__)

@api.route('/login', methods=['POST'])
def login():
  flash('You have been logged in!', 'success')
  return redirect(url_for('main.login'))

@api.route('/logout')
def logout():
  flash('You have been logged out!', 'success')
  return redirect(url_for('main.login'))

@api.route('/register', methods=['POST'])
def register():
  flash('You have been registered!', 'success')
  return redirect(url_for('main.register'))

@main.route('/login')
def login():
  return render_template('login.html', login=True)

@main.route('/')
def index():
  return render_template('index.html')
  

@main.route('/register')
def register():
  return render_template('login.html', login=False)
  
@main.route('/operator')
def operator():
  return render_template('operator.html')

@main.route('/error')
def error():
  return render_template('error.html')

if __name__ == '__main__':
  app.register_blueprint(api, url_prefix='/api')
  app.register_blueprint(main, url_prefix='/')
  app.run('0.0.0.0', debug=True)
