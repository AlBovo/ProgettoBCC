from flask import request, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError
from models import UserManager

def login():
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
        return redirect('main.dashboard')
    
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
    
    if not (user := UserManager.getByEmail(email)): # email not found
        flash('L\'email o la password non è corretta.', category="error")
        return redirect(url_for('main.login'))

    if not check_password_hash(user.get_password(), password): # password incorrect
        flash('L\'email o la password non è corretta.', category="error")
        return redirect(url_for('main.login'))
    
    login_user(user)
    return redirect(url_for('main.dashboard'))