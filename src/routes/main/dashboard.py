from flask import render_template

def dashboard():
    """
    Renders the dashboard page.

    Returns:
        The rendered template for the dashboard page.
    """
    return render_template('dashboard.html')