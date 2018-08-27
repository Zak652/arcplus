import os
from flask import Flask
from flask_admin import Admin, BaseView, expose
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

config_path = os.environ.get("CONFIG_PATH", "arm.config.DevelopmentConfig")
app.config.from_object(config_path)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True 
app.config['USER_ENABLE_EMAIL'] = False

from . import api
from . import views
from . import filters
from . import login

from .database import Base, engine
Base.metadata.create_all(engine)