from flask_login import login_required
from flask import Blueprint
from . import dashboard
from . import index
from . import login
from . import register
from . import ticket

mainbp  =   Blueprint('main', __name__)

mainbp.route('/', methods=['GET'])(index.index)
mainbp.route('/login', methods=['GET'])(login.login)
mainbp.route('/register', methods=['GET'])(register.register)
mainbp.route('/dashboard', methods=['GET'])(login_required(dashboard.dashboard))
mainbp.route('/ticket', methods=['GET'])(login_required(ticket.ticket))
