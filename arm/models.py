import os.path

from flask_admin import Admin, BaseView, expose
from sqlalchemy import Column, Integer, BigInteger, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, ForeignKey

import datetime


from . database import Base

# User Role relationship model
class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

# User Roles object model
class Role(Base, RoleMixin):
    __tablename__ = 'role'

    # User Roles table fields
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    user = relationship("User", secondary = 'roles_users', backref=backref('role'))

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    # Return roles object as dictionary
    def as_dictionary(self):
        roles = {"ID": self.id, "Name": self.name, "Description": self.description}
        return roles

# User object model
class User(Base, UserMixin):
    __tablename__ = 'user'

    # User db table fields
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users'))
    
    def __repr__(self):
        return '<User> {} {}'.format(self.id, self.email)

    # Return user object as dictionary
    def as_dictionary(self):
        users = {"ID": self.id, "User Name": self.username, "Email": self.email, "Role": self.roles, 
                "Last Login": self.last_login_at, "Current Login": self.current_login_at,
                "Last Login IP": self.last_login_ip, "Current Login IP": self.current_login_ip,
                "Login Count": self.login_count, "Active": self.active, "Confirmed At": self.confirmed_at
                }
        return users

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
    purchase_date = Column(DateTime, nullable = True)
    value = Column(Integer, nullable = True)
    photo = Column(String, nullable = True)
    attchments = Column(String, nullable = True)
    notes = Column(String(256), nullable = True)
    captured_by = Column(String(128), nullable = False)
    modified_by = Column(String(128), nullable = False)
    last_verified = Column(DateTime, nullable = True)
    verified_by = Column(String(128), nullable = True)
    category_id = Column(Integer, ForeignKey('asset_categories.id'), nullable = False)
    type_id = Column(Integer, ForeignKey('asset_types.id'), nullable = False)
    model_id = Column(Integer, ForeignKey('asset_models.id'), nullable = False)
    status_id = Column(Integer, ForeignKey('asset_status.id'), nullable = False)
    condition_id = Column(Integer, ForeignKey('asset_condition.id'), nullable = False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable = False)
    costcenter_id = Column(Integer, ForeignKey('cost_centers.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('people.id'), nullable = False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable = False)

    def __repr__ (self):
        return self.name

    #Return asset object as dictionary
    def as_dictionary(self):
        asset={"ID": self.id, "Barcode": self.barcode, "Type": self.asset_type, "Serial No.": self.serial_no, 
                "Location": self.asset_location, "Status": self.asset_status, "Purchase Date": self.purchase_date, 
                "User": self.asset_user, "Purchase Price": self.purchase_price, "Category": self.asset_category, 
                "Name": self.name, "Model": self.asset_model, "Notes": self.notes, "Department": self.asset_center,
                "Captured By": self.captured_by, "Capture Date": self.capture_date, "Cost center": self.asset_center, 
                "Value": self.value, "Supplier": self.asset_supplier, "Attachments": self.attchments, 
                "Modified By": self.modified_by, "Modified Date": self.modified_date, "Last Verified": self.last_verified,
                "Last Verified By": self.verified_by
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
    verified_by = Column(String(128), nullable = False)

    def __repr__(self):
        return self.name
    
    # Return asset verification object as a dictionary
    def as_dictionary(self):
        verification = {"ID": self.id, "Barcode": self.barcode, "Asset Name": self.asset_name,
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
        asset_movement = {"ID": self.id, "Barcode": self.barcode, "Asset Name": self.asset_name,
                        "Moved on" : self.movement_date, "Moved From" : self.moved_from,
                        "Moved To" : self.moved_to
                        }
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
        category = {"ID": self.id, "Category Code": self.category_code, 
                    "Category Name": self.category_name, "Category Types": self.category_type, 
                    "Category Assets": self.asset_category, "Notes": self.notes
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
        _type = {"ID": self.id, "Type Code": self.type_code, "Type Name": self.type_name, 
                "Type Models": self.type_model, "Type Assets": self.asset_type, "Notes": self.notes
                }
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
        _model = {"ID": self.id, "Model Code": self.model_code, "Model Name": self.model_name, 
                "Model Assets": self.asset_model, "Notes": self.notes
                }
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
        status = {"ID": self.id, "Status Code": self.status_code, 
                    "Status Name": self.status_name, "Status Assets": self.asset_status, 
                    "Notes": self.notes
                    }
        return status

# Asset Condition object model
class AssetCondition(Base):
    __tablename__ = 'asset_condition'

    # Asset condition db table fields
    id = Column(Integer, primary_key = True)
    condition_code = Column(String(64), nullable = False, unique = True)
    condition_name = Column(String(128), nullable = False, unique = True)
    notes = Column(String(256), nullable = True)
    asset_condition = relationship ("Asset", backref = "asset_condition")

    def __repr__(self):
        return self.condition_name

    # Return asset condition object as dictionary
    def as_dictionary(self):
        condition = {"ID": self.id, "Condition Code": self.condition_code, 
                    "Condition Name": self.condition_name, "Condition Assets": self.asset_condition, 
                    "Notes": self.notes
                    }
        return condition

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
        location = {"ID": self.id, "Location Code": self.location_code,
                    "Location Name": self.location_name, "Location Assets": self.asset_location, 
                    "People": self.user_location, "Notes": self.notes
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
        cost_center = {"ID": self.id, "Center Code": self.center_code, 
                        "Center Name": self.center_name, "Assets": self.asset_center, 
                        "Notes": self.notes
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
    designation = Column(String(128), nullable = False)
    phone = Column(BigInteger, unique = True)
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
        people = {"ID": self.id, "Personal Code": self.person_code, 
                    "First Name": self.first_name, "Last Name": self.last_name, 
                    "Designation": self.designation, "Department": self.user_department, 
                    "Location": self.user_location, "Phone": self.phone, "Email": self.email,
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
        department = {"ID": self.id, "Department Code": self.department_code,
                                "Department Name": self.department_name, 
                                "People": self.user_department, 
                                "Notes": self.notes
                                }
        return department

# Supplier object model
class Supplier(Base):
    __tablename__ = 'suppliers'

    # Supplier db table fields
    id = Column(Integer, primary_key = True)
    code = Column(String(64), nullable = False, unique = True)
    name = Column(String(128), nullable = False)
    phone = Column(BigInteger, nullable = False, unique = True)
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
        supplier = {"ID": self.id, "Supplier Code": self.code, "Name": self.name, "Category": self.supplier_category,
                        "Phone": self.phone, "Email": self.email, "Location": self.supplier_location,
                        "Website": self.website, "Contact Person": self.supplier_contact, 
                        "Assets Supplied": self.asset_supplier, "Notes": self.notes
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
    supplier_category = relationship ("Supplier", backref = "supplier_category")

    def __repr__(self):
        return self.category_name

    # Return supplier category as dictionary
    def as_dictionary(self):
        supplier_category = {"ID": self.id, "Category Code": self.category_code, "Category Name": self.category_name, 
                            "Category Suppliers": self.supplier_category, "Notes": self.notes
                            }
        return supplier_category