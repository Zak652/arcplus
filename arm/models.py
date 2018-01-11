import os.path

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from . database import Base, engine
from . import app

from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

class Asset(Base):
	__tablename__ = 'assets'

	id = Column(Integer, primary_key = True)
	barcode = Column(String, nullable = False, unique = True)
	serial_no = Column(String, nullable = True)
	capture_date = Column(Datetime, default = datetime.datetime.now)
	name = Column(String(128), nullable = False)
	category = Column(String(128), nullable = False)
	_type = Column(String(128), nullable = False)
	_model = Column(String(128), nullable = True)
	status = Column(String, nullable = False)
	location = Column(String, nullable = False)
	user = Column(String(128), nullable = True)
	purchase_price = Column(Integer, nullable = True)
	value = Column(Integer, nullable = True)
	supplier = Column(String(128), nullable = True)
	photo = Column(nullable = True)
	comments = Column(String(256), nullable = True)

class AssetCategory(Base):
	__tablename__ = 'asset_categories'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)

class AssetType(Base):
	__tablename__ = 'asset_types'

	id = Column(Integer, primary_key = True)
	type_name = Column(String(128), nullable = False, unique = True)

class AssetModel(Base):
	__tablename__ = 'asset_models'

	id = Column(Integer, primary_key = True)
	model_name = Column(String(128), nullable = False, unique = True)

class AssetStatus(Base):
	__tablename__ = 'asset_status'

	id = Column(Integer, primary_key = True)
	status_code = Column(String(64), nullable = False, unique = True)
	status_name = Column(String(128), nullable = False, unique = True)

class Location(Base):
	__tablename__ = 'locations'

	id = Column(Integer, primary_key = True)
	location_code = Column(String(64), nullable = False, unique = True)
	location_name = Column(String(128), nullable = False)

class LocationCategory(Base):
	__tablename__ = 'location_categories'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)

class People(Base):
	__tablename__ = 'people'

	id = Column(Integer, primary_key = True)
	barcode = Column(String(64), nullable = False, unique = True)
	category = Column(String(128), nullable = False)
	first_name = Column(String(128), nullable = False)
	second_name = Column(String(128), nullable = False)
	designation = Column(String(128), nullable = True)
	department = Column(String(128), nullable = False)
	location = Column(String(128), nullable = False)
	phone = Column(Integer, unique = True)
	email = Column(String(128), unique = True)

class PeopleCategory(Base):
	__tablename__ = 'people_category'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)

class Supplier(Base):
	__tablename__ = 'suppliers'

	id = Column(Integer, primary_key = True)
	code = Column(String(64), nullable = False, unique = True)
	category = Column(String(128), nullable = False)
	phone = Column(Integer, nullable = False, unique = True)
	email = Column(String(128), unique = True)
	location = Column(String(128), nullable = False)
	website = Column(String(128), nullable = True, unique = True)
	person = Column(String(128), nullable = True)

class SupplierCategory(Base):
	__tablename__ = 'suppliers_category'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	