from flask import Flask, render_template, url_for, flash, redirect, Blueprint, jsonify, request
from flask_wtf import CSRFProtect
import random, calendar

app = Flask(__name__)
app.config['FRONTEND'] = True
app.config['SECRET_KEY'] = 'gasighoagohsaighaoigshaisgh'
csrf = CSRFProtect(app)
api = Blueprint('api', __name__)
main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

class prova:
  def __init__(self, name, surname):
    self.name = name
    self.surname = surname
    self.is_authenticated = True
  def get_email(self):
    return 'prova@prova.com'
  def get_privilege(self):
    return random.randint(0, 1) == 1
  
@admin.route('/events', methods=['POST'])
def get_operator_day():
  return jsonify([{'start_hour': '830', 'end_hour': '900'}] * 20), 200

@api.route('/login', methods=['POST'])
def login():
  flash('You have been logged in!', 'success')
  return redirect(url_for('main.login'))

@main.route('/ticket', methods=['GET'])
def ticket():
  return render_template('ticket.html')

@api.route('/categories', methods=['GET'])
def categories():
  return jsonify([f'Category {random.randbytes(4).hex()}' for i in range(random.randint(0, 30))]), 200

@api.route('/available', methods=['POST'])
def available():
  return jsonify({'830': [3, 1, 5], '900': [2], '930': [5, 1, 4], '1000': [4, 2, 1]}), 200

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

@api.route('/month', methods=['POST'])
def month():
  data = request.get_json()
  print(data)
  return jsonify([random.randint(0, 100) for i in range(calendar.monthrange(data["year"], data["month"])[1])]), 200

@main.route('/login')
def login():
  return render_template('login.html', login=True, current_user=prova('John', 'Doe'))

@main.route('/')
def index():  
  return render_template('index.html', current_user=prova('John', 'Doe'))

@main.route('/dashboard')
def dashboard():
  return render_template('dashboard.html', current_user=prova('John', 'Doe'), categories=['Category 1', 'Category 2', 'Category 3'])

@main.route('/register')
def register():
  return render_template('login.html', login=False, current_user=prova('John', 'Doe'))
  
@main.route('/operator')
def operator():
  return render_template('operator.html', current_user=prova('John', 'Doe'))

@main.route('/error')
def error():
  return render_template('error.html', status_code=404, error={'message': 'Page not found', 'description': 'The page you are looking for does not exist.'})

if __name__ == '__main__':
  app.register_blueprint(api, url_prefix='/api')
  app.register_blueprint(admin, url_prefix='/admin')
  app.register_blueprint(main, url_prefix='/')
  app.run('0.0.0.0', debug=True)
