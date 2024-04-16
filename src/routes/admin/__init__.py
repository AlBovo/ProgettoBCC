from flask_login import login_required
from flask import Blueprint
from . import events

adminbp  =   Blueprint('admin', __name__)

adminbp.route('/events', methods=['GET'])(login_required(events.get_operator_day))