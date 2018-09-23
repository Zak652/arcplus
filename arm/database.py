from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from . import config

config = config.DevelopmentConfig()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# db_session = scoped_session(session)
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

# from . import models
# # Create DB models from the models file
# Base.metadata.create_all(engine)
