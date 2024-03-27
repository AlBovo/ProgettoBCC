from flask import url_for
from flask_login import LoginManager
from models import UserManager

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "E' necessario aver eseguito il login per accedere alla pagina richiesta."
login_manager.login_message_category = "info"

@login_manager.user_loader
def loadUser(id: str | int):
    return UserManager.get(id)