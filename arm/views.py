from flask import Flask
from flask_login import login_user, logout_user

from . import app
from . database import session, User

# solves most responses you need
from flask import render_template, request, redirect, url_for, flash

# if authentication is needed, this is where you start
from flask_login import login_required, login_user, current_user
from werkzeug.security import check_password_hash

@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')