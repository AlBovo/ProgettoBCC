from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import models
import json
import mysql.connector
import time

# Establish a connection to the MySQL database
connection = mysql.connector.connect( # TODO: insert db info
    host="",
    user="",
    password="",
    database=""
)

cursor = connection.cursor()

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
    """
    Handle the API login request.

    This function is responsible for handling the POST request to the '/login' endpoint of the API.
    It validates the email and password provided in the request form, checks if the user is already authenticated,
    and redirects the user to the appropriate page based on the validation results.

    Returns:
        A redirect response to the dashboard page if the user is already authenticated.
        A redirect response to the login page with appropriate error messages if the email or password is missing,
        the email is not in a valid format, the password is too short, or the email or password is incorrect.
        A redirect response to the dashboard page if the email and password are correct and the user is successfully logged in.
    """
    if current_user.is_authenticated:
        return redirect('/dashboard')
    
    email = request.form.get('email', type=str)
    password = request.form.get('password', type=str)
    
    if not email or not password:
        flash('E\' necessario inserire un\'email ed una password.', category="error")
        return redirect(url_for('main.login'))
    
    try:
        validate_email(email)
    except EmailNotValidError as e: # TODO : decide if we want to show the error message to the user
        flash('L\'email non ha un formato valido.', category="error")
        return redirect(url_for('main.login'))
    
    if len(password) < 8:
        flash('La password deve essere lunga almeno 8 caratteri.', category="error")
        return redirect(url_for('main.login'))
    
    if not (user := models.Users.getByEmail(email)):
        flash('L\'email o la password non è corretta.', category="error")
        return redirect(url_for('main.login'))

    if not check_password_hash(user.get_password(), password):
        flash('L\'email o la password non è corretta.', category="error")
        return redirect(url_for('main.login'))
    
    login_user(user)
    return redirect(url_for('main.dashboard'))

@apibp.route('/register', methods=['POST'])
def api_register():
    """
    Register a new user through the API.

    This function handles the registration process for a new user. It checks if the user is already authenticated,
    retrieves the email, password, and password confirmation from the request form, and performs various validations
    on the input data. If any validation fails, an appropriate error message is flashed and the user is redirected
    to the registration page.

    Returns:
        A redirect response to the dashboard page if the user is already authenticated.
        A redirect response to the register page with appropriate error messages if the email or password is missing,
        the email is not in a valid format, the password is too short, or the email or password is incorrect.
        A redirect response to the login page if the email and password are correct and the user is successfully logged in.    
    """
    if current_user.is_authenticated:
        return redirect('/dashboard')
    
    email = request.form.get('email', type=str)
    password = request.form.get('password', type=str)
    password_confirm = request.form.get('password_confirm', type=str)
    
    if not email or not password or not password_confirm:
        flash('E\' necessario inserire un\'email ed una password.', category="error")
        return redirect(url_for('main.register'))
    
    if password != password_confirm:
        flash('Le password non corrispondono.', category="error")
        return redirect(url_for('main.register'))
    
    try:
        validate_email(email)
    except EmailNotValidError as e: # TODO : decide if we want to show the error message to the user
        flash('L\'email non ha un formato valido.', category="error")
        return redirect(url_for('main.login'))
    
    if len(password) < 8:
        flash('La password deve essere lunga almeno 8 caratteri.', category="error")
        return redirect(url_for('main.register'))
    
    if not models.Users.add(email, generate_password_hash(password)):
        flash('L\'email è già usata da un altro account.', category="error")
        return redirect(url_for('main.register'))
    
    flash('Registrazione effettuata con successo.', category="success")
    return redirect(url_for('main.login'))

@apibp.route('/logout')
def api_logout():
    """
    Logout the user by removing the 'session' key from the session object.
    
    Returns:
        Redirect the user to the home page after logout.
    """
    logout_user()
    return redirect(url_for('main.index'))

@apibp.route('/month', methods=['POST'])
@login_required
def get_month():
    #event query response: [id, Month, day, start_hour, end_hour, user_id, Operator]
    Operator = request.cookies.get('Operator', type=int) #gets the id of the operator from the cookies
    Operator = int(Operator) if Operator is not None else None
    Month = time.localtime().tm_mon                      #gets current month

    data = []
    counter = 0
    previousDay = 0

    query = "SELECT * FROM EVENTS WHERE OPERATOR = %s AND MONTH = %s"
    cursor.execute(query, (Operator, Month))

    for event in cursor.fetchall():
        if previousDay == 0:
            previousDay = event[1]

        if event[1] == previousDay:
            counter += 1
            
        else:
            data.append(json.dumps(
                {
                    "day":previousDay,
                    "events Number":counter
                }))
                
            counter = 1
            previousDay = event[1]
    
    return jsonify(data) # return data

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