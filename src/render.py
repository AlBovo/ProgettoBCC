from flask import Flask, render_template, url_for, flash, redirect, Blueprint, jsonify
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

@api.route('/day', methods=['POST'])
def day():
  return jsonify([{'start_hour': '830', 'end_hour': '900'}] * 20), 200

@main.route('/login')
def login():
  return render_template('login.html', login=True)

@main.route('/')
def index():
  return render_template('index.html', current_user='palle')

@main.route('/dashboard')
def dashboard():
  return render_template('dashboard.html')

@main.route('/register')
def register():
  return render_template('login.html', login=False)
  
@main.route('/operator')
def operator():
  return render_template('operator.html')

@main.route('/error')
def error():
  return render_template('error.html', status_code=404, error={'message': 'Page not found', 'description': 'The page you are looking for does not exist.'})

if __name__ == '__main__':
  app.register_blueprint(api, url_prefix='/api')
  app.register_blueprint(main, url_prefix='/')
  app.run('0.0.0.0', debug=True)
