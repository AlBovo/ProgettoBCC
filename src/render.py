from flask import Flask, render_template, url_for, flash, redirect, Blueprint

app = Flask(__name__)
app.config['FRONTEND'] = True
app.config['SECRET_KEY'] = 'gasighoagohsaighaoigshaisgh'
api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
  flash('You have been logged in!', 'success')
  return redirect(url_for('login'))

@api.route('/logout', methods=['POST'])
def apiLogout():
  flash('You have been logged out!', 'success')
  return redirect(url_for('login'))

@api.route('/register', methods=['POST'])
def apiRegister():
  flash('You have been registered!', 'success')
  return redirect(url_for('register'))

@app.route('/login')
def login():
  return render_template('login.html', login=True)

@app.route('/logout')
def logout():
  flash('You have been logged out!', 'success')
  return redirect(url_for('login'))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register')
def register():
  return render_template('login.html', login=False)
  
@app.route('/operator')
def operator():
  return render_template('operator.html')

if __name__ == '__main__':
  app.register_blueprint(api, url_prefix='/api')
  app.run('0.0.0.0', debug=True)
