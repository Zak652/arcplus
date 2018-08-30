from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request
from flask_login import login_required, login_user, current_user, LoginManager, logout_user

from . import app, decorators, models, views

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('user') == 'Admin'
        # return session.get(current_user) == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('dashboard', next=request.url))
