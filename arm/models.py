import os.path

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from . database import Base, engine, session
from . import app

import datetime

from flask_login import UserMixin
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# User object model
class User(Base, UserMixin):
    __tablename__ = 'users'

    # User db table fields
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable = False)
    email = Column(String(128), nullable = False, unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable = False)
    password = Column(String(128), nullable = False)
    
    def __repr__(self):
        return self.name

    # Return user object as dictionary
    def as_dictionary(self):
        users = {"id": self.id, "Name": self.name, "Email": self.email, "Role": self.user_role}
        return users


# User Roles object model
class Role(Base):
    __tablename__ = 'roles'

    # User Roles table fields
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable = False, unique = True)
    role_desc = Column(String(256), nullable = False)
    user = relationship("User", backref = "user_role")

    def __repr__(self):
        return self.name

    # Return roles object as dictionary
    def as_dictionary(self):
        roles = {"id": self.id, "Name": self.name, "Description": self.role_desc}
        return roles


# Asset object model
class Asset(Base):
    __tablename__ = 'assets'

    # Asset db table fields
    id = Column(Integer, primary_key = True)
    barcode = Column(String(20), nullable = False, unique = True)
    asset_no = Column(String(20), nullable = False, unique = True)
    serial_no = Column(String, nullable = True)
    capture_date = Column(DateTime, default = datetime.datetime.now)
    modified_date = Column(DateTime, default = datetime.datetime.now, onupdate = datetime.datetime.utcnow)
    name = Column(String(128), nullable = False)
    purchase_price = Column(Integer, nullable = True)
    value = Column(Integer, nullable = True)
    photo = Column(String, nullable = True)
    attchments = Column(String, nullable = True)
    notes = Column(String(256), nullable = True)
    captured_by = Column(String(128), nullable = False)
    modified_by = Column(String(128), nullable = False)
    category_id = Column(Integer, ForeignKey('asset_categories.id'), nullable = False)
    type_id = Column(Integer, ForeignKey('asset_types.id'), nullable = False)
    model_id = Column(Integer, ForeignKey('asset_models.id'), nullable = False)
    status_id = Column(Integer, ForeignKey('asset_status.id'), nullable = False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable = False)
    costcenter_id = Column(Integer, ForeignKey('cost_centers.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('people.id'), nullable = False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable = False)

    def __repr__ (self):
        return self.name

    #Return asset object as dictionary
    def as_dictionary(self):
        asset={"Id": self.id, "Barcode": self.barcode, "Serial No.": self.serial_no,
                "Capture Date": self.capture_date, "modified Date": self.modified_date, 
                "Name": self.name, "Category": self.asset_category, "Type": self.asset_type, 
                "Model": self.asset_model, "Status": self.asset_status, 
                "Location": self.asset_location, "Cost center": self.asset_center, 
                "User": self.asset_user, "Purchase Price": self.purchase_price, 
                "Value": self.value, "Supplier": self.asset_supplier, "Photo": self.photo, 
                "Attachements": self.attchments, "Notes": self.notes,
                "Captured By": self.captured_by, "Modified By": self.modified_by
                }
        return asset


# Asset Verification
class AssetVerification(Base):
    __tablename__ = 'asset_verifications'

    # Asset verification db table fields
    id = Column(Integer, primary_key = True)
    barcode = Column(String(20), nullable = False)
    asset_name = Column(String(128), nullable = False)
    verification_date = Column(DateTime, default = datetime.datetime.now)
    verified_by = Column(String(128), nullable = True)

    def __repr__(self):
        return self.name
    
    # Return asset verification object as a dictionary
    def as_dictionary(self):
        verification = {"Id": self.id, "Barcode": self.barcode, "Asset Name": self.asset_name,
                        "Verification Date": self.verification_date
                        }
        return verification


# Asset Movement
class AssetMovement(Base):
    __tablename__ = 'asset_movements'

    # Asset verification db table fields
    id = Column(Integer, primary_key = True)
    barcode = Column(String(20), nullable = False)
    asset_name = Column(String(128), nullable = False)
    movement_date = Column(DateTime, default = datetime.datetime.now)
    moved_from = Column(String(128), nullable = False)
    moved_to = Column(String(128), nullable = False)
    moved_by = Column(String(128), nullable = False)

    def __repr__(self):
        return self.name
    
    # Return asset verification object as a dictionary
    def as_dictionary(self):
        asset_movement = {"Id": self.id, "Barcode": self.barcode, "Asset Name": self.asset_name,
                        "Moved on" : self.movement_date, "Moved From" : self.moved_from,
                        "Moved To" : self.moved_to}
        return asset_movement


# Asset Category object model
class AssetCategory(Base):
    __tablename__ = 'asset_categories'

    # Asset category db table fields
    id = Column(Integer, primary_key = True)
    category_code = Column(String(128), nullable = False, unique = True)
    category_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    category_type = relationship ("AssetType", backref = "category_type")
    asset_category = relationship("Asset", backref = "asset_category")

    def __repr__(self):
        return self.category_name

    # Return asset category object as dictionary
    def as_dictionary(self):
        category = {"id": self.id, "Category Code": self.category_code, 
                    "Category Name": self.category_name, "Notes": self.notes
                    }
        return category

# Asset Type object model
class AssetType(Base):
    __tablename__ = 'asset_types'

    # Asset types db table fields
    id = Column(Integer, primary_key = True)
    type_code = Column(String(128), nullable = False, unique = True)
    type_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    category_id = Column(Integer, ForeignKey('asset_categories.id'), nullable = False)
    asset_type = relationship ("Asset", backref = "asset_type")
    type_model = relationship ("AssetModel", backref = "type_model")

    def __repr__(self):
        return self.type_name

    # Return asset type object as dictionary
    def as_dictionary(self):
        _type = {"id": self.id, "Type_name": self.type_name, "Notes": self.notes}
        return _type

# Asset Model object model
class AssetModel(Base):
    __tablename__ = 'asset_models'

    # Asset model db table fields
    id = Column(Integer, primary_key = True)
    model_code = Column(String(128), nullable = False, unique = True)
    model_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    model_type = Column(Integer, ForeignKey('asset_types.id'), nullable = True)
    asset_model = relationship ("Asset", backref = "asset_model")

    def __repr__(self):
        return self.model_name

    # Return asset model object as dictionary
    def as_dictionary(self):
        _model = {"id": self.id, "model_name": self.model_name, "Notes": self.notes}
        return _model

# Asset Status object model
class AssetStatus(Base):
    __tablename__ = 'asset_status'

    # Asset status db table fields
    id = Column(Integer, primary_key = True)
    status_code = Column(String(64), nullable = False, unique = True)
    status_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    asset_status = relationship ("Asset", backref = "asset_status")

    def __repr__(self):
        return self.status_name

    # Return asset status object as dictionary
    def as_dictionary(self):
        status = {"id": self.id, "status_code": self.status_code, 
                    "status_name": self.status_name, "Notes": self.notes
                    }
        return status

# Asset Locations object model
class Location(Base):
    __tablename__ = 'locations'

    # Asset locations db table fields
    id = Column(Integer, primary_key = True)
    location_code = Column(String(64), nullable = False, unique = True)
    location_name = Column(String(128), nullable = False)
    notes = Column(String(256), nullable = True)
    asset_location = relationship ("Asset", backref = "asset_location")
    user_location = relationship ("People", backref = "user_location")
    supplier_location = relationship ("Supplier", backref = "supplier_location")

    def __repr__(self):
        return self.location_name

    # Return asset location object as dictionary
    def as_dictionary(self):
        location = {"id": self.id, "location_code": self.location_code,
                    "location_name": self.location_name, "Notes": self.notes
                    }
        return location

# Cost Centers Object model
class CostCenter(Base):
    __tablename__ = 'cost_centers'

    # Cost Centers db table fields
    id = Column(Integer, primary_key = True)
    center_code = Column(String(64), nullable = False, unique = True)
    center_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    asset_center = relationship ("Asset", backref = "asset_center")

    def __repr__(self):
        return self.center_name

    # Return cost center as dictionary
    def as_dictionary(self):
        cost_center = {"id": self.id, "Center Code": self.center_code, 
                        "Center Name": self.center_name, "Notes": self.notes
                        }
        return cost_center

# People object model
class People(Base):
    __tablename__ = 'people'

    # People db table fields
    id = Column(Integer, primary_key = True)
    person_code = Column(String(64), nullable = False, unique = True)
    first_name = Column(String(128), nullable = False)
    last_name = Column(String(128), nullable = False)
    designation = Column(String(128), nullable = True)
    phone = Column(Integer, unique = True)
    email = Column(String(128), unique = True)
    notes = Column(String(256), nullable = True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable = False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable = False)
    asset_user = relationship ("Asset", backref = "asset_user")
    supplier_contact = relationship ("Supplier", backref = "supplier_contact")

    def __repr__(self):
        return self.first_name

    # Return people as dictionary
    def as_dictionary(self):
        people = {"id": self.id, "Personal Code": self.person_code, 
                    "First Name": self.first_name, "Last Name": self.last_name, 
                    "Designation": self.designation, "Department": self.department_id, 
                    "Location": self.location_id, "Phone": self.phone, "Email": self.email,
                    "User Assets": self.asset_user, "Notes": self.notes
                    }
        return people

# Department object model
class Department(Base):
    __tablename__ = "departments"

    # Department db table fields
    id = Column(Integer, primary_key = True)
    department_code = Column(String(64), nullable = True, unique = True)
    department_name = Column(String(128), nullable = False)
    notes = Column(String(256), nullable = True)
    user_department = relationship ("People", backref = "user_department")

    def __repr__(self):
        return self.department_name

    # Return department as dictionary
    def as_dictionary(self):
        department = {"id": self.id, "department_code": self.department_code,
                                "department_name": self.department_name, "Notes": self.notes
                                }
        return department

# Supplier object model
class Supplier(Base):
    __tablename__ = 'suppliers'

    # Supplier db table fields
    id = Column(Integer, primary_key = True)
    code = Column(String(64), nullable = False, unique = True)
    name = Column(String(128), nullable = False)
    phone = Column(Integer, nullable = False, unique = True)
    email = Column(String(128), unique = True)
    website = Column(String(128), nullable = True, unique = True)
    notes = Column(String(256), nullable = True)
    category_id = Column(Integer, ForeignKey("supplier_categories.id"), nullable = False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable = False)
    contact_person = Column(Integer, ForeignKey("people.id"), nullable = True)
    asset_supplier = relationship ("Asset", backref = "asset_supplier")

    def __repr__(self):
        return self.name

    # Return supplier as dictionary
    def as_dictionary(self):
        supplier = {"id": self.id, "code": self.code, "category": self.supplier_category,
                        "phone": self.phone, "email": self.email, "location": self.supplier_location,
                        "website": self.website, "Notes": self.notes
                        }
        return supplier

# Supplier category model
class SupplierCategory(Base):
    __tablename__ = 'supplier_categories'

    # Supplier category db table fields
    id = Column(Integer, primary_key = True)
    category_code = Column(String(20), nullable = False, unique = True)
    category_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    supplier_category = relationship ("Supplier", backref = "supplier_category", lazy = True)

    def __repr__(self):
        return self.category_name

    # Return supplier category as dictionary
    def as_dictionary(self):
        supplier_category = {"id": self.id, "category_name": self.category_name, 
                            "Category_code": self.category_code, "Notes": self.notes
                            }
        return supplier_category


db_adapter = SQLAlchemyAdapter(db, User)
# Setup Flask-User and specify the User data-model
user_manager = UserManager(db_adapter, app)

admin = Admin(app)
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Role, session))
admin.add_view(ModelView(Asset, session))
