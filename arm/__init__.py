import os
from flask import Flask, redirect, url_for
from flask_security import Security, SQLAlchemySessionUserDatastore
from .models import User, Role
from .database import db_session, init_db, session
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "arm.config.DevelopmentConfig")
app.config.from_object(config_path)

db = SQLAlchemy

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

mail = Mail(app)

Bootstrap(app)

from . import api
from . import decorators
from . import views
from . import filters
from . import login
from . import admin

# Load the database
init_db()