import os.path

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base, engine
from . import app

import datetime

from flask_login import UserMixin

# User object model
class User(Base, UserMixin):
    __tablename__ = 'users'

    # User db table fields
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    
    def __repr__(self):
        return self.name

    # Return user object as dictionary
    def as_dictionary(self):
        users = {"id": self.id, "Name": self.name, "Email": self.email}
        return users

# Asset object model
class Asset(Base):
    __tablename__ = 'assets'

    # Asset db table fields
    id = Column(Integer, primary_key = True)
    barcode = Column(String, nullable = False, unique = True)
    serial_no = Column(String, nullable = True)
    capture_date = Column(DateTime, default = datetime.datetime.now)
    modified_date = Column(DateTime, default = datetime.datetime.now, onupdate = datetime.datetime.utcnow)
    name = Column(String(128), nullable = False)
    purchase_price = Column(Integer, nullable = True)
    value = Column(Integer, nullable = True)
    photo = Column(String, nullable = True)
    attchments = Column(String, nullable = True)
    notes = Column(String(256), nullable = True)
    category_id = Column(Integer, ForeignKey('asset_categories.id'), nullable = True)
    category = relationship("AssetCategory", backref = "asset_category")
    type_id = Column(Integer, ForeignKey('asset_types.id'), nullable = True)
    _type = relationship("AssetType", backref = "asset_type")
    model_id = Column(Integer, ForeignKey('asset_models.id'), nullable = True)
    _model = relationship("AssetModel", backref = "asset_model")
    status_id = Column(Integer, ForeignKey('asset_status.id'), nullable = True)
    status = relationship("AssetStatus", backref = "asset_status")
    location_id = Column(Integer, ForeignKey('locations.id'), nullable = True)
    location = relationship("Location", backref = "asset_location")
    costcenter_id = Column(Integer, ForeignKey('cost_centers.id'), nullable = True)
    cost_center = relationship("CostCenter", backref = "asset_costcenter")
    user_id = Column(Integer, ForeignKey('people.id'), nullable = True)
    user = relationship("People", backref = "asset_user")
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable = True)
    supplier = relationship("Supplier", backref = "asset_supplier")

    def __repr__ (self):
        return self.name


    #Return asset object as dictionary
    def as_dictionary(self):
        asset={"Id": self.id, "Barcode": self.barcode, "Serial No.": self.serial_no,
                "Capture Date": self.capture_date, "modified Date": self.modified_date, 
                "Name": self.name, "Category": self.category.category_name,
                "Type": self._type.type_name, "Model": self._model.model_name, 
                "Status": self.status.status_name, "Location": self.location.location_name, 
                "Cost center": self.cost_center.center_name, "User": self.user.first_name, 
                "Purchase Price": self.purchase_price, "Value": self.value, 
                "Supplier": self.supplier.name, "Photo": self.photo, "Attachements": self.attchments, 
                "Notes": self.notes
                }
        return asset


# Asset Category object model
class AssetCategory(Base):
    __tablename__ = 'asset_categories'

    # Asset category db table fields
    id = Column(Integer, primary_key = True)
    category_code = Column(String(128), nullable = False, unique = True)
    category_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    category_type = relationship ("AssetType", backref = "category_type")
    category_assets = relationship("Asset", backref = "category_assets")

    def __repr__(self):
        return self.category_name

    # Return asset category object as dictionary
    def as_dictionary(self):
        categories = {"id": self.id, "Category Name": self.category_name, "Notes": self.notes}
        return categories

# Asset Type object model
class AssetType(Base):
    __tablename__ = 'asset_types'

    # Asset type db table fields
    id = Column(Integer, primary_key = True)
    type_code = Column(String(128), nullable = False, unique = True)
    type_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    type_category = Column(Integer, ForeignKey('asset_categories.id'), nullable = False)
    type_model = relationship ("AssetModel", backref = "type_model")
    type_assets = relationship ("Asset", backref = "type_assets")

    def __repr__(self):
        return self.type_name

    # Return asset type object as dictionary
    def as_dictionary(self):
        _types = {"id": self.id, "type_name": self.type_name, "Notes": self.notes}
        return _types

# Asset Model object model
class AssetModel(Base):
    __tablename__ = 'asset_models'

    # Asset model db table fields
    id = Column(Integer, primary_key = True)
    model_code = Column(String(128), nullable = False, unique = True)
    model_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    model_type = Column(Integer, ForeignKey('asset_types.id'), nullable = True)
    model_assets = relationship ("Asset", backref = "asset_model")

    def __repr__(self):
        return self.model_name

    # Return asset model object as dictionary
    def as_dictionary(self):
        _models = {"id": self.id, "model_name": self.model_name, "Notes": self.notes}
        return _models

# Asset Status object model
class AssetStatus(Base):
    __tablename__ = 'asset_status'

    # Asset status db table fields
    id = Column(Integer, primary_key = True)
    status_code = Column(String(64), nullable = False, unique = True)
    status_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    status_assets = relationship ("Asset", backref = "asset_status")

    def __repr__(self):
        return self.status_name

    # Return asset status object as dictionary
    def as_dictionary(self):
        _status ={"id": self.id, "status_code": self.status_code, 
                    "status_name": self.status_name, "Notes": self.notes
                    }
        return _status

# Asset Location object model
class Location(Base):
    __tablename__ = 'locations'

    # Asset location db table fields
    id = Column(Integer, primary_key = True)
    location_code = Column(String(64), nullable = False, unique = True)
    location_name = Column(String(128), nullable = False)
    notes = Column(String(256), nullable = True)
    location_assets = relationship ("Asset", backref = "location_assets")
    location_people = relationship ("People", backref = "location_people")

    def __repr__(self):
        return self.location_name

    # Return asset locations object as dictionary
    def as_dictionary(self):
        _locations ={"id": self.id, "location_code": self.location_code,
                    "location_name": self.location_name, "Notes": self.notes,
                    "category": self.category
                    }
        return _locations

# Cost Centers Object model
class CostCenter(Base):
    __tablename__ = 'cost_centers'

    # Cost Centers db table fields
    id = Column(Integer, primary_key = True)
    center_code = Column(String(64), nullable = False, unique = True)
    center_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    center_assets = relationship ("Asset", backref = "center_assets")

    def __repr__(self):
        return self.center_name

    # Return asset locations categories as dictionary
    def as_dictionary(self):
        cost_centers = {"id": self.id, "Center Code": self.center_code, 
                        "Center Name": self.center_name, "Notes": self.notes
                        }
        return cost_centers

# People object model
class People(Base):
    __tablename__ = 'people'

    # People db table fields
    id = Column(Integer, primary_key = True)
    barcode = Column(String(64), nullable = False, unique = True)
    category = Column(Integer, ForeignKey("people_categories.id"), nullable = False)
    first_name = Column(String(128), nullable = False)
    last_name = Column(String(128), nullable = False)
    designation = Column(String(128), nullable = True)
    department = Column(Integer, ForeignKey("departments.id"), nullable = False)
    location = Column(Integer, ForeignKey("locations.id"), nullable = False)
    phone = Column(Integer, unique = True)
    email = Column(String(128), unique = True)
    notes = Column(String(256), nullable = True)
    user_assets = relationship ("Asset", backref = "user_assets")

    def __repr__(self):
        return self.first_name

    # Return people as dictionary
    def as_dictionary(self):
        _people = {"id": self.id, "Barcode": self.barcode, "Category": self.category, 
                    "First Name": self.first_name, "Last Name": self.last_name, 
                    "Designation": self.designation, "Department": self.department, 
                    "Location": self.location, "Phone": self.phone, "Email": self.email,
                    "Notes": self.notes
                    }
        return _people

# People Category object model
class PeopleCategory(Base):
    __tablename__ = 'people_categories'

    # People category db table fields
    id = Column(Integer, primary_key = True)
    category_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    category_people = relationship ("People", backref = "person_category")

    def __repr__(self):
        return self.category_name

    # Return People categories as dictionary
    def as_dictionary(self):
        people_category = {"id": self.id, "category_name": self.category_name, "Notes": self.notes}
        return people_category

# Department object model
class Department(Base):
    __tablename__ = "departments"

    # Department db table fields
    id = Column(Integer, primary_key = True)
    department_code = Column(String(64), nullable = True, unique = True)
    department_name = Column(String(128), nullable = False)
    notes = Column(String(256), nullable = True)
    department_people = relationship ("People", backref = "person_department")

    def __repr__(self):
        return self.department_name

    # Return departments as dictionary
    def as_dictionary(self):
        _departments = {"id": self.id, "department_code": self.department_code,
                                "department_name": self.department_name, "Notes": self.notes
                                }
        return _departments

# Supplier object model
class Supplier(Base):
    __tablename__ = 'suppliers'

    # Supplier db table fields
    id = Column(Integer, primary_key = True)
    code = Column(String(64), nullable = False, unique = True)
    name = Column(String(128), nullable = False)
    category = Column(Integer, ForeignKey("suppliers_category.id"), nullable = False)
    phone = Column(Integer, nullable = False, unique = True)
    email = Column(String(128), unique = True)
    location = Column(Integer, ForeignKey("locations.id"), nullable = False)
    website = Column(String(128), nullable = True, unique = True)
    notes = Column(String(256), nullable = True)
    person = Column(Integer, ForeignKey("people.id"), nullable = True)
    supplier_assets = relationship ("Asset", backref = "asset_supplier")

    def __repr__(self):
        return self.name

    # Return suppliers as dictionary
    def as_dictionary(self):
        _suppliers = {"id": self.id, "code": self.code, "category": self.category,
                        "phone": self.phone, "email": self.email, "location": self.location,
                        "website": self.website, "Notes": self.notes
                        }
        return _suppliers

# Supplier category model
class SupplierCategory(Base):
    __tablename__ = 'suppliers_category'

    # Supplier category db table fields
    id = Column(Integer, primary_key = True)
    category_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    category_suppliers = relationship ("Supplier", backref = "supplier_category")

    def __repr__(self):
        return self.category_name

    # Return supplier categories as dictionary
    def as_dictionary(self):
        supplier_categories = {"id": self.id, "category_name": self.category_name, "Notes": self.notes}
        return supplier_categories