import os.path

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base, engine
from . import app

import datetime

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
	capture_date = Column(DateTime, default = datetime.datetime.now)
	name = Column(String(128), nullable = False)
	category = Column(Integer, ForeignKey('asset_categories.id'), nullable = True)
	_type = Column(Integer, ForeignKey('asset_types.id'), nullable = True)
	_model = Column(Integer, ForeignKey('asset_models.id'), nullable = True)
	status = Column(Integer, ForeignKey('asset_status.id'), nullable = True)
	location = Column(Integer, ForeignKey('locations.id'), nullable = True)
	user = Column(Integer, ForeignKey('people.id'), nullable = True)
	purchase_price = Column(Integer, nullable = True)
	value = Column(Integer, nullable = True)
	supplier = Column(Integer, ForeignKey('suppliers.id'), nullable = True)
	photo = Column(String, nullable = True)
	comments = Column(String(256), nullable = True)

	#Return asset object as dictionary
	def as_dictionary(self):
		asset={"id": self.id, "barcode": self.barcode, "serial_no": self.serial_no,
				"capture_date": self.capture_date, "name": self.name, "category": self.category,
				"_type": self._type, "_model": self._model, "status": self.status,
				"location": self.location, "user": self.user, "purchase_price": self.purchase_price,
				"value": self.value, "supplier": self.supplier, "photo": self.photo,
				"comments": self.comments
				}
		return asset


class AssetCategory(Base):
	__tablename__ = 'asset_categories'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_assets = relationship("Asset", backref = "asset_category")

	def as_dictionary(self):
		categories = {"id": self.id, "category_name": self.category_name}
		return categories

class AssetType(Base):
	__tablename__ = 'asset_types'

	id = Column(Integer, primary_key = True)
	type_name = Column(String(128), nullable = False, unique = True)
	type_assets = relationship ("Asset", backref = "asset_type")

	def as_dictionary(self):
		_types = {"id": self.id, "type_name": self.type_name}
		return _types

class AssetModel(Base):
	__tablename__ = 'asset_models'

	id = Column(Integer, primary_key = True)
	model_name = Column(String(128), nullable = False, unique = True)
	model_assets = relationship ("Asset", backref = "asset_model")

	def as_dictionary(self):
		_models = {"id": self.id, "model_name": self.model_name}
		return _models

class AssetStatus(Base):
	__tablename__ = 'asset_status'

	id = Column(Integer, primary_key = True)
	status_code = Column(String(64), nullable = False, unique = True)
	status_name = Column(String(128), nullable = False, unique = True)
	status_assets = relationship ("Asset", backref = "asset_status")

	def as_dictionary(self):
		_statuses ={"id": self.id, "status_code": self.status_code, 
					"status_name": self.status_name
					}
		return _statuses

class Location(Base):
	__tablename__ = 'locations'

	id = Column(Integer, primary_key = True)
	location_code = Column(String(64), nullable = False, unique = True)
	location_name = Column(String(128), nullable = False)
	category = Column(Integer, ForeignKey("location_categories.id"), nullable = True)
	location_assets = relationship ("Asset", backref = "asset_location")
	location_people = relationship ("People", backref = "person_location")

	def as_dictionary(self):
		_locations ={"id": self.id, "location_code": self.location_code,
					"location_name": self.location_name,
					"category": self.category
					}
		return _locations

class LocationCategory(Base):
	__tablename__ = 'location_categories'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_locations = relationship ("Location", backref = "location_category")

	def as_dictionary(self):
		_locations_categories = {"id": self.id, "category_name": self.category_name}
		return _locations_categories

class People(Base):
	__tablename__ = 'people'

	id = Column(Integer, primary_key = True)
	barcode = Column(String(64), nullable = False, unique = True)
	category = Column(Integer, ForeignKey("people_categories.id"), nullable = False)
	first_name = Column(String(128), nullable = False)
	second_name = Column(String(128), nullable = False)
	designation = Column(String(128), nullable = True)
	department = Column(Integer, ForeignKey("departments.id"), nullable = False)
	location = Column(Integer, ForeignKey("locations.id"), nullable = False)
	phone = Column(Integer, unique = True)
	email = Column(String(128), unique = True)

class PeopleCategory(Base):
	__tablename__ = 'people_categories'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_people = relationship ("People", backref = "person_category")

	def as_dictionary(self):
		people_category = {"id": self.id, "category_name": self.category_name}
		return people_category

class Department(Base):
	__tablename__ = "departments"

	id = Column(Integer, primary_key = True)
	department_code = Column(String(64), nullable = True, unique = True)
	department_name = Column(String(128), nullable = False)
	department_people = relationship ("People", backref = "person_department")

	def as_dictionary(self):
		_departments = {"id": self.id, "department_code": self.department_code,
								"department_name": self.department_name
								}
		return _departments

class Supplier(Base):
	__tablename__ = 'suppliers'

	id = Column(Integer, primary_key = True)
	code = Column(String(64), nullable = False, unique = True)
	category = Column(Integer, ForeignKey("suppliers_category.id"), nullable = False)
	phone = Column(Integer, nullable = False, unique = True)
	email = Column(String(128), unique = True)
	location = Column(Integer, ForeignKey("locations.id"), nullable = False)
	website = Column(String(128), nullable = True, unique = True)
	person = Column(Integer, ForeignKey("people.id"), nullable = True)

	def as_dictionary(self):
		_suppliers = {"id": self.id, "code": self.code, "category": self.category,
						"phone": self.phone, "email": self.email, "location": self.location,
						"website": self.website
						}
		return _suppliers

class SupplierCategory(Base):
	__tablename__ = 'suppliers_category'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_suppliers = relationship ("Supplier", backref = "supplier_category")

	def as_dictionary(self):
		supplier_categories = {"id": self.id, "category_name": self.category_name}
		return supplier_categories
