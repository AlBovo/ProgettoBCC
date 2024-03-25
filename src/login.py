from flask import url_for
from flask_login import LoginManager
from models import Users

login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = "Perfavore esegua il login per accedere alla pagina richiesta."
login_manager.login_message_category = "info"
@login_manager.user_loader
def loadUser(id: str | int):
    return Users.get(id)