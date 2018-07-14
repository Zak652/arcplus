from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin

from . import app, models

import datetime

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Create DB models from the models file
Base.metadata.create_all(engine)
