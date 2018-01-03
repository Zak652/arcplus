from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin

from . import app

import datetime

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
