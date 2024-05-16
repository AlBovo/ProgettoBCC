from flask_login import login_required
from flask import Blueprint
from . import add_event
from . import chat
from . import day
from . import delete_event
from . import login
from . import logout
from . import month
from . import question
from . import register
from . import week
from . import categories

apibp  =   Blueprint('api', __name__)

apibp.route('/add_event', methods=['POST'])(login_required(add_event.add_event))
# apibp.route('/chat', methods=['POST'])(login_required(add_event.add_event))
apibp.route('/day', methods=['POST'])(login_required(day.get_day))
apibp.route('/delete_event', methods=['POST'])(login_required(delete_event.delete_event))
apibp.route('/login', methods=['POST'])(login.login)
apibp.route('/logout', methods=['GET'])(logout.logout)
apibp.route('/month', methods=['POST'])(login_required(month.get_month))
apibp.route('/question', methods=['POST'])(login_required(question.ask_question))
apibp.route('/register', methods=['POST'])(register.register)
apibp.route('/week', methods=['POST'])(login_required(week.get_week))
apibp.route('/categories', methods=['GET'])(login_required(categories.get_categories))
