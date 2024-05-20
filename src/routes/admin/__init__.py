from flask_login import login_required
from flask import Blueprint
from . import events
from . import stats

adminbp  =   Blueprint('admin', __name__)

adminbp.route('/events', methods=['GET'])(login_required(events.get_operator_day))
adminbp.route('/stats', methods=['POST'])(login_required(stats.operator_stats))