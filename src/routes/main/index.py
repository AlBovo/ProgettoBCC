from flask import render_template, redirect, url_for
from flask_login import current_user

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