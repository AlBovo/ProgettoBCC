from flask import request, redirect, url_for, flash
from flask_login import current_user
from werkzeug.security import generate_password_hash
from email_validator import validate_email, EmailNotValidError
from models import UserManager

def register():
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
    
    if not UserManager.add(email, generate_password_hash(password)):
        flash('L\'email è già usata da un altro account.', category="error")
        return redirect(url_for('main.register'))
    
    flash('Registrazione effettuata con successo.', category="success")
    return redirect(url_for('main.login'))