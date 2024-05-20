from flask import redirect, url_for
from flask_login import logout_user

def logout():
    """
    Logout the user by removing the 'session' key from the session object.
    
    Returns:
        Redirect the user to the home page after logout.
    """
    logout_user()
    return redirect(url_for('main.index'))