from flask_login import LoginManager
from flask import redirect, url_for
from flask_security import url_for_security

from . import app, models
from . database import session

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_get"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
	return session.query(models.User).get(int(id))