from flask import Blueprint
from . import events

adminbp  =   Blueprint('admin', __name__)

adminbp.route('/events', methods=['GET'])(events.get_operator_day)