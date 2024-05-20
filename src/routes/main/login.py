from flask import render_template

def login():
    """
    Renders the login.html template.

    Returns:
        The rendered login.html template.
    """
    return render_template('login.html', login=True)