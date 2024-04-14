from flask import Flask, render_template, url_for, flash, redirect

app = Flask(__name__)
app.config['FRONTEND'] = True
app.config['SECRET_KEY'] = 'gasighoagohsaighaoigshaisgh'

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/logout')
def logout():
  flash('You have been logged out!', 'success')
  return redirect(url_for('login'))

@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/register')
def register():
  return render_template('register.html')
  
@app.route('/operator')
def operator():
  return render_template('operator.html')

if __name__ == '__main__':
  app.run('0.0.0.0', debug=True)
