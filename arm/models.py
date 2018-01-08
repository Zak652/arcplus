import os.path

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from . database import Base, engine
from . import app


class Asset(Base):
	__tablename__ = 'assets'

	id = Column(Integer, primary_key = True)
	barcode = Column(String, nullable = False)
	serial_no = Column(String, nullable = True)
	datetime = Column(Datetime, default = datetime.datetime.now)
	name = Column(String(128), nullable = False)
	category = Column(String(128), nullable = False)
	_type = Column(String(128), nullable = False)
	_model = Column(String(128), nullable = True)
	status = Column(String, nullable = False)
	location = Column(String, nullable = False)
	user = Column(String(128), nullable = True)
	cost = Column(Integer, nullable = True)
	value = Column(Integer, nullable = True)
	supplier = Column(String(128), nullable = True)
	photo = Column()
	comments = Column(String(256))



