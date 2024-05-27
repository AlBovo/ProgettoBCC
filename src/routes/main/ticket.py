from flask import render_template

def ticket():
    """
    Renders the ticket page.

    Returns:
        The rendered template for the ticket page.
    """
    return render_template('ticket.html')