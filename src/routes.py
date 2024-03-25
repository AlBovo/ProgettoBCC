from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, logout_user, login_user, current_user
from hashlib import sha256
import json, models

mainbp  =   Blueprint('main', __name__)
apibp   =   Blueprint('api', __name__)
adminbp =   Blueprint('admin', __name__)

@mainbp.route('/')
def index():
    """
    Renders the index page.

    If the current user is authenticated, it redirects to the dashboard page.
    Otherwise, it renders the login page.

    Returns:
        The rendered template for the index page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    else:
        return render_template('index.html')
    
@mainbp.route('/login')
def login():
    """
    Renders the login.html template.

    Returns:
        The rendered login.html template.
    """
    return render_template('login.html')

@mainbp.route('/register')
def register():
    """
    Renders the register.html template.

    Returns:
        The rendered register.html template.
    """
    return render_template('register.html')

@mainbp.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the dashboard page.

    Returns:
        The rendered template for the dashboard page.
    """
    return render_template('dashboard.html')



@apibp.route('/login', methods=['POST'])
def api_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if len(email) == 0 or len(password) == 0:
        return json.dumps({'error': 'E\' necessario inserire un\'email ed una password.'})
    
    # if not EMAIL_REGEX.match(email):
    #     return redirect('/login') # TODO : add error message
    
    if not (user := models.Users.getByEmail(email)):
        return json.dumps({'error': 'L\'email o la password non è corretta.'})
    
    if user.hashPassword == sha256(password.encode()).hexdigest():
        return json.dumps({'error': 'L\'email o la password non è corretta.'})
    
    login_user(user)
    return redirect('/')

@apibp.route('/register', methods=['POST'])
def api_register():
    # TODO: add logic
    return redirect('/')

@apibp.route('/logout')
def api_logout():
    """
    Logout the user by removing the 'session' key from the session object.
    
    Returns:
        Redirect the user to the home page after logout.
    """
    logout_user()
    return redirect('/')

@apibp.route('/month', methods=['POST'])
@login_required
def get_month():
    # TODO: add logic
    return redirect('/') # return data

@apibp.route('/day', methods=['POST'])
@login_required
def get_day():
    # TODO: add logic
    return redirect('/') # return data

@apibp.route('/add_event', methods=['POST'])
@login_required
def add_event():
    # TODO: add logic
    return redirect('/') # return data

@apibp.route('/delete_event', methods=['POST'])
@login_required
def delete_event():
    # TODO: add logic
    return redirect('/') # return data

@apibp.route('/question', methods=['POST'])
@login_required
def question():
    # TODO: add logic
    return redirect('/') # return data

# @apibp.route('/chat', methods=['POST'])
# @login_required
# def chatbot():
#     return redirect('/') # return data