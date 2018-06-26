import os
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

config_path = os.environ.get("CONFIG_PATH", "arm.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import api
from . import views
from . import filters
from . import login

from .database import Base, engine
Base.metadata.create_all(engine)