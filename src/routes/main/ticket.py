from flask import render_template
from flask_login import current_user
from models import TicketManager
def ticket():
    """
    Renders the ticket page.

    Returns:
        The rendered template for the ticket page.
    """

    ticket = TicketManager.getTicket(current_user.get_id())
    return render_template('ticket.html')