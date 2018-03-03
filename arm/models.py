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
	category = Column(Integer, nullable = True)
	_type = Column(Integer, nullable = True)
	_model = Column(Integer, nullable = True)
	status = Column(Integer, nullable = True)
	location = Column(Integer, nullable = True)
	user = Column(Integer, nullable = True)
	purchase_price = Column(Integer, nullable = True)
	value = Column(Integer, nullable = True)
	supplier = Column(Integer, nullable = True)
	photo = Column(String, nullable = True)
	comments = Column(String(256), nullable = True)

	#Return asset object as dictionary
	def as_dictionary(self):
		asset={"Id": self.id, "Barcode": self.barcode, "Serial No.": self.serial_no,
				"Capture Date": self.capture_date, "Name": self.name, "Category": self.category,
				"Type": self._type, "Model": self._model, "Status": self.status,
				"Location": self.location, "User": self.user, "Purchase Price": self.purchase_price,
				"Value": self.value, "Supplier": self.supplier, "Photo": self.photo,
				"Comments": self.comments
				}
		return asset


class AssetCategory(Base):
	__tablename__ = 'asset_categories'

	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	# category_assets = relationship("Asset", backref = "asset_category")

	def as_dictionary(self):
		categories = {"id": self.id}
		return categories
