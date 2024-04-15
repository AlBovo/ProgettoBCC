from flask import render_template

def register():
    """
    Renders the register.html template.

    Returns:
        The rendered register.html template.
    """
    return render_template('login.html', login=False)