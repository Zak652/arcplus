from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import login_user, current_user, LoginManager, logout_user, login_required
from flask_security import login_required, roles_required
from sqlalchemy.exc import SQLAlchemyError, DataError
import datetime

from flask_bootstrap import Bootstrap

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, decorators, models
from .database import session
from flask_sqlalchemy import SQLAlchemy
from flask_security import LoginForm, url_for_security

@app.context_processor
def login_context():
    return {
        'url_for_security': url_for_security,
        'login_user_form': LoginForm()
		}

# Start route and Authentication

#Appliction requires login from the start
@app.route("/")
# @login_required
def index():
	""" Application requires users to login first.
		All initial access is redirected to login page.
	"""
	return redirect(url_for("login_get"))

@app.route("/admin/")
@login_required
def admin_panel():
	""" Admin Panel requires Admin role for access
	"""
	if not current_user.has_role('Admin'):
		# return False
		return redirect(url_for('logout'))
	return redirect('/admin/users')


# Views for Adding New Users, Users Login and Logout

# New User registration. Get user information
@app.route("/user/add", methods = ["GET"])
@login_required
@roles_required('Admin')
def create_user():
	""" Display user registration form """

	#Get asset categories from DB
	roles_list = session.query(models.Role).order_by(models.Role.id)

	return render_template("add_user.html", roles_list = roles_list)

# Verify user information and register new user
@app.route("/user/add", methods = ["POST"])
@login_required
@roles_required('Admin')
def add_user():

	if request.method == 'POST':
		username = request.form['name']
		email = request.form['email']
		#check if email is unique / doesn't exist already
		if session.query(models.User).filter_by(email=email).first():
			flash("User with that email address already exists", "danger")
			return redirect(url_for("create_user"))
		roles = request.form['role']
		role = session.query(models.Role).filter_by(name=roles).first()
		password = request.form['password']
		#Check if password is not less than 8 characters
		if len(password) < 8:
			flash("Password should be 8 or more characters long")
			return redirect(url_for("create_user"))

	# Add users to DB
	new_user = models.User(username=username, email = email,
							password = generate_password_hash(password))

	session.add(new_user)
	new_user.roles = [role]
	try:
		session.commit()
		flash('New user added successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

	return redirect(url_for("create_user"))

# User Login Access
@app.route("/user/login")
def login_get():
	""" Provide login form and collect login credentials """
	return render_template("/security/login_user.html")


#Logout User
@app.route("/user/logout")

# @login_required
def logout():
	logout_user()
	return redirect(url_for("login_get"))

# Dashboard display / user landing page
# Display a graphical summary of the app data

# User change password route
@app.route("/user/change_password")
@login_required
def change_password():
	"""
	provide users with the a form to change their password
	"""
	return render_template("security/change_password.html")

# Dashboard
@app.route("/dashboard")
@login_required

def dashboard():
	"""
	The dashboard is graphical display of data using statistical tiles,
	graphs and data tables
	"""
	return render_template("dashboard.html")

# views for Viewing full asset register, Single asset, Creating New Asset,
# Modifying Asset details and Deleting existing Asset

# Full Register view route
@app.route("/register/view", methods = ["GET"])
@login_required
def view_register():
	"""
	Queries the database for all assets and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get assets from DB
	register = session.query(models.Asset).order_by(models.Asset.barcode)

	#Convert register to a list of dictionary items
	assets = [asset.as_dictionary() for asset in register]

    #Pass dictionary list into html render function
	return render_template("view_register.html", assets = assets)

# Single asset view route
@app.route("/register/view/<barcode>", methods = ["GET"])
@login_required

def view_single_asset(barcode):
	"""
	Queries the database for all assets and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for asset
	asset_search = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()

	#Convert result into a list of dictionary items
	asset = [result.as_dictionary() for result in asset_search]

	#Pass asset info into html render function
	return render_template("single_asset.html", asset = asset)

# Create new asset route
@app.route("/register/add_asset", methods = ["GET"])
@login_required

def create_asset():
	"""	Provides empty form to be filled with asset details	"""

	#Get asset categories from DB
	categories_list = session.query(models.AssetCategory).order_by(models.AssetCategory.category_code)

	#Get asset types from DB
	types_list = session.query(models.AssetType).order_by(models.AssetType.type_code)

	#Get asset models from DB
	models_list = session.query(models.AssetModel).order_by(models.AssetModel.model_code)

	#Get asset statuses from DB
	statuses_list = session.query(models.AssetStatus).order_by(models.AssetStatus.status_code)

	#Get asset conditions from DB
	conditions_list = session.query(models.AssetCondition).order_by(models.AssetCondition.condition_code)

	#Get locations from DB
	locations_list = session.query(models.Location).order_by(models.Location.location_code)

	#Get cost centers from DB
	costcenters_list = session.query(models.CostCenter).order_by(models.CostCenter.center_code)

	#Get Users from DB
	users_list = session.query(models.People).order_by(models.People.person_code)

	#Get suppliers from DB
	suppliers_list = session.query(models.Supplier).order_by(models.Supplier.code)

	return render_template("add_asset.html", categories_list = categories_list,
							types_list = types_list, models_list = models_list,
							statuses_list = statuses_list, locations_list = locations_list,
							costcenters_list = costcenters_list, users_list = users_list,
							suppliers_list = suppliers_list, conditions_list = conditions_list
							)

# Post New Asset information
@app.route("/register/add_asset", methods = ["POST"])
@login_required

def add_asset():
	"""
	Captures new asset information and
	creates an entry in the database
	"""
	#Capture new asset details
	if request.method == 'POST':
		barcode = request.form['barcode'],
		#Check if Barcode is unique
		if session.query(models.Asset).filter_by(barcode=barcode).first():
			flash("An asset with Barcode: {} already exists".format(barcode), "danger")
			return redirect(url_for("create_asset"))
		asset_no = request.form['barcode'],
		serial_no = request.form['serial_no'],
		name = request.form['name'],
		category_id = request.form['category'],
		type_id = request.form['_type'],
		model_id = request.form['_model'],
		status_id = request.form['status'],
		condition_id = request.form['condition'],
		location_id = request.form['location'],
		costcenter_id = request.form['cost_center'],
		user_id = request.form['user'],

		#Check if purchase price is not blank
		purchase_price = None,
		if len(request.form['purchase_price']) != 0:
			purchase_price = request.form['purchase_price']

		#Check if purchase date is not blank
		purchase_date = None,
		if len(request.form['purchase_date']) != 0:
			purchase_date = request.form['purchase_date']

		#Check if ref_No is not blank
		ref_No = None,
		if len(request.form['ref_no']) !=0:
			ref_No = request.form['ref_no']

		supplier_id = request.form['supplier'],
		notes = request.form["notes"],
		captured_by = current_user.username,
		modified_by = current_user.username

	new_asset = models.Asset(barcode=barcode, asset_no=asset_no, serial_no=serial_no, name=name,
							category_id=category_id, type_id=type_id, model_id=model_id, status_id=status_id,
							location_id=location_id, costcenter_id=costcenter_id, user_id=user_id,
							purchase_price=purchase_price, purchase_date=purchase_date, supplier_id=supplier_id,
							notes=notes, captured_by=captured_by, modified_by=modified_by, ref_No=ref_No,
							condition_id=condition_id
							)

	#Add entry to database
	session.add(new_asset)
	try:
		session.commit()
		flash('New asset with Barcode: {} added to the register successfully!'.format(barcode), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to asset register
	return redirect(url_for("create_asset"))

# Modify Existing Asset
@app.route("/register/edit/asset/<barcode>", methods=["GET"])
@login_required

def edit_asset(barcode):
	""" Provide form populated with asset information to be edited """

	#Get asset categories from DB
	categories_list = session.query(models.AssetCategory).order_by(models.AssetCategory.category_code)

	#Get asset types from DB
	types_list = session.query(models.AssetType).order_by(models.AssetType.type_code)

	#Get asset models from DB
	models_list = session.query(models.AssetModel).order_by(models.AssetModel.model_code)

	#Get asset statuses from DB
	statuses_list = session.query(models.AssetStatus).order_by(models.AssetStatus.status_code)

	#Get asset conditions from DB
	conditions_list = session.query(models.AssetCondition).order_by(models.AssetCondition.condition_code)

	#Get locations from DB
	locations_list = session.query(models.Location).order_by(models.Location.location_code)

	#Get cost centers from DB
	costcenters_list = session.query(models.CostCenter).order_by(models.CostCenter.center_code)

	#Get Users from DB
	users_list = session.query(models.People).order_by(models.People.barcode)

	#Get suppliers from DB
	suppliers_list = session.query(models.Supplier).order_by(models.Supplier.code)

	asset = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()
	asset = asset[0]

	return render_template("edit_asset.html", id = asset.id, barcode = asset.barcode,
							serial_no = asset.serial_no, name = asset.name,
							category = asset.category, _type = asset._type,
							_model = asset._model, status = asset.status,
							location = asset.location, cost_center = asset.cost_center,
							user = asset.user, supplier = asset.supplier,
							purchase_price = asset.purchase_price, notes = asset.notes,
							categories_list = categories_list, types_list = types_list,
							models_list = models_list, statuses_list = statuses_list,
							conditions_list = conditions_list, locations_list = locations_list,
							costcenters_list = costcenters_list, users_list = users_list,
							suppliers_list = suppliers_list
							)

# POST Asset Modifications
@app.route("/register/edit/asset/<barcode>", methods=['POST'])
@login_required

def update_asset(barcode):
	"""
	Captures updated asset information and
	posts updated information to the database
	"""
	asset = session.query(models.Asset).filter(models.Asset.barcode == barcode).first()
	asset.barcode = request.form["barcode"]
	asset.serial_no = request.form["serial_no"]
	asset.name = request.form["name"]
	asset.category = request.form["category"]
	asset._type = request.form["_type"]
	asset._model = request.form["_model"]
	asset.status = request.form["status"]
	asset.location = request.form["location"]
	asset.cost_center = request.form["cost_center"]
	asset.user = request.form["user"]
	asset.purchase_price = request.form["purchase_price"]
	temp = request.form["value"]
	if temp != '':
		asset.value = 0
	else:
		try:
			sent = int(temp)
		except (ValueError):
			sent = 0

	asset.value = sent
	asset.supplier = request.form["supplier"]
	asset.photo = request.form["photo"]
	asset.notes = request.form["notes"]

	session.add(asset)
	try:
		session.commit()
		flash('Asset details updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset register
	return redirect(url_for("view_register"))

# Delete asset from register
@app.route("/register/delete/asset/<barcode>")
@login_required

def asset_to_delete(barcode):
	"""
	Identify asset to be deleted bassed on provided barcode
	"""
    #Query database for asset
	asset_search = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()
	asset = [result.as_dictionary() for result in asset_search]
	asset = asset[0]

    #Display the asset details for confirmation
	return render_template("delete_asset.html", asset = asset)

# Delete asset from database
@app.route("/register/deleted/<barcode>")
@login_required

def delete_asset(barcode):
	"""
	Search for confirmed asset and deletes it from the database
	"""
    #Search database for asset
	asset = session.query(models.Asset).filter(models.Asset.barcode == barcode).first()

    #Delete asset from database
	session.delete(asset)
	try:
		session.commit()
		flash('Asset with barcode ' + asset.barcode + ' deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset register
	return redirect(url_for("view_register"))


# Views for Asset verification
@app.route("/register/verification", methods = ['GET'])
@login_required
def asset_verification():

	return render_template("verify_asset.html")

# Get asset to be verified
@app.route("/register/verification", methods = ['POST'])
@login_required
def verify_asset():
	# Get barcode to verify
	barcode = request.form['barcode']

	# Check if barcode exists
	barcode_search = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()

	if barcode_search:
		#Convert result into a list of dictionary items
		asset = [result.as_dictionary() for result in barcode_search]

		# Update verification table
		verified = models.AssetVerification(barcode = asset[0]['Barcode'],
		asset_name = asset[0]['Name'], verified_by = current_user.username)

		# Update Asset record
		asset_verified = session.query(models.Asset).filter(models.Asset.barcode == barcode).first()
		asset_verified.barcode = barcode
		#Add entry to database
		session.add(verified)
		try:
			session.commit()
			flash('Barcode: '+ asset[0]['Barcode'] +' verified.', category='message')
		except SQLAlchemyError as error:
			flash('Something went wrong, please make sure your information is correct.', category='error')
			session.rollback
			raise error

		#Pass asset info into html render function
		return render_template("verified_asset.html", asset = asset)

	else:
		flash('Asset with barcode: ' + barcode + ' is not on registered, capture asset.', category='message')
		return redirect(url_for("create_asset"))


# Views to view Full list of Asset Categories, Single Asset Category,
# Create New Category, Modify Existing Category details, Delete Existing Category

#Route to view full list of asset categories
@app.route("/asset_categories/view", methods = ["GET"])
@login_required

def view_asset_categories():
	"""
	Queries the database for all assets categories and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get assets categories from DB
	categories = session.query(models.AssetCategory).order_by(models.AssetCategory.id)

	#Convert categories to a list of dictionary items
	category_list = [category.as_dictionary() for category in categories]

    #Pass dictionary list into html render function
	return render_template("view_categories.html", category_list = category_list)

#Single Asset Category view route
@app.route("/asset_categories/view/<category_code>", methods = ["GET"])
@login_required

def view_asset_category(category_code):
	"""
	Queries the database for all categories and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for category
	category_search = session.query(models.AssetCategory).filter(models.AssetCategory.category_code == category_code).all()

	#Convert result into a list of dictionary items
	category = [result.as_dictionary() for result in category_search]

	#Pass asset info into html render function
	return render_template("single_category.html", category = category)

#Create new asset category route
@app.route("/asset_categories/add_asset_category", methods = ["GET"])
@login_required

def create_asset_category():
	"""	Provides empty form to be filled with new asset category details	"""

	return render_template("add_category.html")

@app.route("/asset_categories/add_asset_category", methods = ["POST"])
@login_required

def add_asset_category():
	"""
	Captures new asset category information and
	creates an entry in the database
	"""
	#Capture new asset category details
	if request.method == 'POST':
		category_code = request.form['code'],
		#Check if Category code is unique
		if session.query(models.AssetCategory).filter_by(category_code=category_code).first():
			flash("Category code: {} is in use by another category".format(category_code), "danger")
			return redirect(url_for("create_asset_category"))

		category_name = request.form['name']

	new_asset_category = models.AssetCategory(
			category_code = category_code,
			category_name = category_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_category)
	try:
		session.commit()
		flash('New asset category; {} added successfully!'.format(category_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'error')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to asset register
	return redirect(url_for("create_asset_category"))

# Modify Existing Asset Category
@app.route("/asset_categories/edit/asset_category/<category_code>", methods=["GET"])
@login_required

def edit_asset_category(category_code):
	""" Provide form populated with asset category information to be edited """

	category = session.query(models.AssetCategory).filter(models.AssetCategory.category_code == category_code).all()
	category = category[0]

	return render_template("edit_category.html", id = category.id,
		category_code = category.category_code,
		category_name = category.category_name,
		notes = category.notes
    	)

# POST Asset Category Modifications
@app.route("/asset_categories/edit/asset_category/<category_code>", methods=['POST'])
@login_required

def update_asset_category(category_code):
	"""
	Captures updated asset category information and
	posts updated information to the database
	"""
	category = session.query(models.AssetCategory).filter(models.AssetCategory.category_code == category_code).first()
	category.category_code = request.form["code"]
	category.category_name = request.form["name"]
	category.notes = request.form["notes"]

	session.add(category)
	try:
		session.commit()
		flash(category.name + ' Category updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset categories
	return redirect(url_for("view_asset_categories"))

# Delete asset category
@app.route("/asset_categories/delete_category/<category_code>")
@login_required

def category_to_delete(category_code):
	"""
	Identify category to be deleted bassed on provided category code
	"""
    #Query database for category
	category_search = session.query(models.AssetCategory).filter(models.AssetCategory.category_code == category_code).all()
	category = [result.as_dictionary() for result in category_search]
	category = category[0]

    #Display the category details for confirmation
	return render_template("delete_category.html", category = category)

# Delete asset category from database
@app.route("/asset_categories/deleted/<category_code>")
@login_required

def delete_asset_category(category_code):
	"""
	Search for confirmed asset category and deletes it from the database
	"""
    #Search database for asset category
	category = session.query(models.AssetCategory).filter(models.AssetCategory.category_code == category_code).first()

    #Delete asset category from database
	session.delete(category)
	try:
		session.commit()
		flash(category.name + ' Category deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset categories view
	return redirect(url_for("view_asset_categories"))


# Views to view Full list of Asset Types, Single Asset Type,
# Create New Type, Modify Existing Type details, Delete Existing Type

#Route to view full list of asset types
@app.route("/asset_types/view", methods = ["GET"])
@login_required

def view_asset_types():
	"""
	Queries the database for all assets types and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get asset types from DB
	types_reg = session.query(models.AssetType).order_by(models.AssetType.id)

	#Convert types_reg to a list of dictionary items
	types_list = [types.as_dictionary() for types in types_reg]

    #Pass dictionary list into html render function
	return render_template("view_types.html", types_list = types_list)

#Single Asset type view route
@app.route("/asset_types/view/<type_code>", methods = ["GET"])
@login_required
def view_asset_type(type_code):
	"""
	Queries the database for all asset types and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for asset types
	type_search = session.query(models.AssetType).filter(models.AssetType.type_code == type_code).all()

	#Convert result into a list of dictionary items
	types_list = [result.as_dictionary() for result in type_search]

	#Pass asset info into html render function
	return render_template("single_type.html", types_list = types_list)

#Create new asset type route
@app.route("/asset_types/add_asset_type", methods = ["GET"])
@login_required

def create_asset_type():
	"""	Provides empty form to be filled with new asset type details	"""

	#Get asset categories from DB
	categories = session.query(models.AssetCategory).order_by(models.AssetCategory.category_code)

	return render_template("add_type.html", categories = categories)

@app.route("/asset_types/add_asset_type", methods = ["POST"])
@login_required

def add_asset_type():
	"""
	Captures new asset type information and
	creates an entry in the database
	"""
	#Capture new asset type details
	if request.method == 'POST':
		type_code = request.form['code'],
		#Check if Type code is unique
		if session.query(models.AssetType).filter_by(type_code=type_code).first():
			flash("Type code: {} is in use by another Asset Type".format(type_code), "danger")
			return redirect(url_for("create_asset_type"))

		type_name = request.form['name']

	new_asset_type = models.AssetType(
			type_code = type_code,
			type_name = type_name,
			category_id = request.form['type_category'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_type)
	try:
		session.commit()
		flash('New asset type; {} added successfully!'.format(type_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to create type form
	return redirect(url_for("create_asset_type"))

# Modify Existing Asset Type
@app.route("/asset_types/edit/asset_type/<type_code>", methods=["GET"])
@login_required
def edit_asset_type(type_code):
	""" Provide form populated with asset model information to be edited """

	types_search = session.query(models.AssetType).filter(models.AssetType.type_code_code == type_code).all()
	_type = types_search[0]

	return render_template("edit_asset_type.html", id = _type.id,
		type_code = _type.type_code,
		type_name = _type.type_name,
		notes = _type.notes
    	)

# POST Asset Type Modifications
@app.route("/asset_types/edit/asset_type/<type_code>", methods=['POST'])
@login_required

def update_asset_type(type_code):
	"""
	Captures updated asset type information and
	posts updated information to the database
	"""
	_type = session.query(models.AssetType).filter(models.AssetType.type_code == type_code).first()
	_type.type_code = request.form["code"]
	_type.type_name = request.form["name"]
	_type.type_category = request.form["type_category"]
	_type.notes = request.form["notes"]

	session.add(_type)
	try:
		session.commit()
		flash(_type.name + ' asset type updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset types
	return redirect(url_for("view_asset_types"))

# Delete asset type
@app.route("/asset_type/delete_type/<type_code>")
@login_required

def type_to_delete(type_code):
	"""
	Identify type to be deleted bassed on provided type code
	"""
    #Query database for type
	type_search = session.query(models.AssetType).filter(models.AssetType.type_code == type_code).all()
	_type = [result.as_dictionary() for result in type_search]
	_type = _type[0]

    #Display the Type details for confirmation
	return render_template("delete_type.html", _type = _type)

# Delete asset type from database
@app.route("/asset_type/deleted/<type_code>")
@login_required

def delete_asset_type(type_code):
	"""
	Search for confirmed asset type and deletes it from the database
	"""
    #Search database for asset type
	_type = session.query(models.AssetType).filter(models.AssetType.type_code == type_code).first()

    #Delete asset type from database
	session.delete(_type)
	try:
		session.commit()
		flash(_type.name + ' asset type deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset types view
	return redirect(url_for("view_asset_types"))


# Views to view Full list of Asset Models, Single Asset Model,
# Create New Model, Modify Existing Model details, Delete Existing Model

#Route to view full list of asset models
@app.route("/asset_models/view", methods = ["GET"])
@login_required

def view_asset_models():
	"""
	Queries the database for all assets models and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get assets models from DB
	models_reg = session.query(models.AssetModel).order_by(models.AssetModel.id)

	#Convert models_reg to a list of dictionary items
	models_list = [model.as_dictionary() for model in models_reg]

    #Pass dictionary list into html render function
	return render_template("view_models.html", models_list = models_list)

#Single Asset model view route
@app.route("/asset_models/view/<model_code>", methods = ["GET"])
@login_required

def view_asset_model(model_code):
	"""
	Queries the database for all models and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for model
	model_search = session.query(models.AssetModel).filter(models.AssetModel.model_code == model_code).all()

	#Convert result into a list of dictionary items
	model = [result.as_dictionary() for result in model_search]

	#Pass asset info into html render function
	return render_template("single_model.html", model = model)

#Create new asset model route
@app.route("/asset_models/add_asset_model", methods = ["GET"])
@login_required

def create_asset_model():
	"""	Provides empty form to be filled with new asset model details	"""

	#Get asset types from DB
	types_list = session.query(models.AssetType).order_by(models.AssetType.type_code)

	return render_template("add_model.html", types_list = types_list)

@app.route("/asset_models/add_asset_model", methods = ["POST"])
@login_required

def add_asset_model():
	"""
	Captures new asset model information and
	creates an entry in the database
	"""
	#Capture new asset model details
	if request.method == 'POST':
		model_code = request.form['code'],
		#Check if Category code is unique
		if session.query(models.AssetModel).filter_by(model_code=model_code).first():
			flash("Model code: {} is in use by another Asset Model".format(model_code), "danger")
			return redirect(url_for("create_asset_category"))

		model_name = request.form['name']

	new_asset_model = models.AssetModel(
			model_code = model_code,
			model_name = model_name,
			model_type = request.form['model_type'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_model)
	try:
		session.commit()
		flash('New asset model; {} added successfully!'.format(model_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to asset register
	return redirect(url_for("create_asset_model"))

# Modify Existing Asset Model
@app.route("/asset_models/edit/asset_model/<model_code>", methods=["GET"])
@login_required

def edit_asset_model(model_code):
	""" Provide form populated with asset model information to be edited """

	model = session.query(models.AssetModel).filter(models.AssetModel.model_code == model_code).all()
	model = model[0]

	return render_template("edit_asset_model.html", id = model.id,
		model_code = model.model_code,
		model_name = model.model_name,
		notes = model.notes
    	)

# POST Asset Model Modifications
@app.route("/asset_models/edit/asset_model/<model_code>", methods=['POST'])
@login_required

def update_asset_model(model_code):
	"""
	Captures updated asset model information and
	posts updated information to the database
	"""
	model = session.query(models.AssetModel).filter(models.AssetModel.model_code == model_code).first()
	model.model_code = request.form["code"]
	model.model_name = request.form["name"]
	model.model_type = request.form["model_type"]
	model.notes = request.form["notes"]

	session.add(model)
	try:
		session.commit()
		flash(model.name + ' Model updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset models
	return redirect(url_for("view_asset_models"))

# Delete asset models
@app.route("/asset_models/delete_model/<model_code>")
@login_required

def model_to_delete(model_code):
	"""
	Identify model to be deleted bassed on provided model code
	"""
    #Query database for model
	model_search = session.query(models.AssetModel).filter(models.AssetModel.model_code == model_code).all()
	model = [result.as_dictionary() for result in model_search]
	model = model[0]

    #Display the model details for confirmation
	return render_template("delete_model.html", model = model)

# Delete asset model from database
@app.route("/asset_model/deleted/<model_code>")
@login_required

def delete_asset_model(model_code):
	"""
	Search for confirmed asset model and deletes it from the database
	"""
    #Search database for asset model
	model = session.query(models.AssetModel).filter(models.AssetModel.model_code == model_code).first()

    #Delete asset model from database
	session.delete(model)
	try:
		session.commit()
		flash(model.name + ' Model deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset models view
	return redirect(url_for("view_asset_models"))


# Views to view Full list of Asset Status, Single Asset Status,
# Create New Status, Modify Existing Status details, Delete Existing Status

#Route to view full list of asset Status
@app.route("/asset_status/view", methods = ["GET"])
@login_required

def view_asset_statuses():
	"""
	Queries the database for all assets status and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get assets status from DB
	status_reg = session.query(models.AssetStatus).order_by(models.AssetStatus.id)

	#Convert Status_reg to a list of dictionary items
	status_list = [status.as_dictionary() for status in status_reg]

    #Pass dictionary list into html render function
	return render_template("view_statuses.html", status_list = status_list)

#Single Asset status view route
@app.route("/asset_status/view/<status_code>", methods = ["GET"])
@login_required

def view_status(status_code):
	"""
	Queries the database for all status and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for status
	status_search = session.query(models.AssetStatus).filter(models.AssetStatus.status_code == status_code).all()

	#Convert result into a list of dictionary items
	status = [status.as_dictionary() for status in status_search]

	#Pass status info into html render function
	return render_template("single_status.html", status = status)

#Create new asset status route
@app.route("/asset_status/add_asset_status", methods = ["GET"])
@login_required

def create_asset_status():
	"""	Provides empty form to be filled with new asset status details	"""

	return render_template("add_status.html")

@app.route("/asset_status/add_asset_status", methods = ["POST"])
@login_required

def add_asset_status():
	"""
	Captures new asset status information and
	creates an entry in the database
	"""
	#Capture new asset category details
	if request.method == 'POST':
		status_code = request.form['code'],
		#Check if Category code is unique
		if session.query(models.AssetStatus).filter_by(status_code=status_code).first():
			flash("Status code: {} is in use by another Asset Status".format(status_code), "danger")
			return redirect(url_for("create_asset_status"))

		status_name = request.form['name']

	new_asset_status = models.AssetStatus(
			status_code = status_code,
			status_name = status_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_status)
	try:
		session.commit()
		flash('New asset status; {} added successfully!'.format(status_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to asset register
	return redirect(url_for("create_asset_status"))

# Modify Existing Asset Status
@app.route("/asset_status/edit_asset_status/<status_code>", methods=["GET"])
@login_required

def edit_asset_status(status_code):
	""" Provide form populated with asset status information to be edited """

	status = session.query(models.AssetStatus).filter(models.AssetStatus.status_code == status_code).all()
	status = status[0]

	return render_template("edit_asset_status.html", id = status.id,
		status_code = status.status_code,
		status_name = status.status_name,
		notes = status.notes
    	)

# POST Asset Status Modifications
@app.route("/asset_status/edit/asset_status/<status_code>", methods=['POST'])
@login_required

def update_asset_status(status_code):
	"""
	Captures updated asset status information and
	posts updated information to the database
	"""
	status = session.query(models.AssetStatus).filter(models.AssetStatus.status_code == status_code).first()
	status.status_code = request.form["code"]
	status.staus_name = request.form["name"]
	status.notes = request.form["notes"]

	session.add(status)
	try:
		session.commit()
		flash(status.name + ' Satus updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset status
	return redirect(url_for("view_asset_status"))

# Delete asset status
@app.route("/asset_status/delete_status/<status_code>")
@login_required

def status_to_delete(status_code):
	"""
	Identify status to be deleted bassed on provided status code
	"""
    #Query database for status
	status_search = session.query(models.AssetStatus).filter(models.AssetStatus.status_code == status_code).all()
	status = [result.as_dictionary() for result in status_search]
	status = status[0]

    #Display the status details for confirmation
	return render_template("delete_status.html", status = status)

# Delete asset status from database
@app.route("/asset_status/deleted/<status_code>")
@login_required

def delete_asset_status(status_code):
	"""
	Search for confirmed asset status and deletes it from the database
	"""
    #Search database for asset status
	status = session.query(models.AssetStatus).filter(models.AssetStatus.status_code == status_code).first()

    #Delete asset status from database
	session.delete(status)
	try:
		session.commit()
		flash(status.name + ' Status deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset status view
	return redirect(url_for("view_asset_status"))


# Views to view Full list of Asset condition, Single Asset condition,
# Create New condition, Modify Existing condition details, Delete Existing condition

#Route to view full list of asset condition
@app.route("/asset_condition/view", methods = ["GET"])
@login_required

def view_asset_conditions():
	"""
	Queries the database for all assets condition and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get assets condition from DB
	conditions_reg = session.query(models.AssetCondition).order_by(models.AssetCondition.id)

	#Convert condition_reg to a list of dictionary items
	conditions_list = [condition.as_dictionary() for condition in conditions_reg]

    #Pass dictionary list into html render function
	return render_template("view_conditions.html", conditions_list = conditions_list)

#Single Asset condition view route
@app.route("/asset_condition/view/<condition_code>", methods = ["GET"])
@login_required

def view_condition(condition_code):
	"""
	Queries the database for all condition and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for condition
	condition_search = session.query(models.AssetCondition).filter(models.AssetCondition.condition_code == condition_code).all()

	#Convert result into a list of dictionary items
	condition = [condition.as_dictionary() for condition in condition_search]

	#Pass condition info into html render function
	return render_template("single_condition.html", condition = condition)

#Create new asset condition route
@app.route("/asset_condition/add_asset_condition", methods = ["GET"])
@login_required

def create_asset_condition():
	"""	Provides empty form to be filled with new asset condition details	"""

	return render_template("add_condition.html")

@app.route("/asset_condition/add_asset_condition", methods = ["POST"])
@login_required

def add_asset_condition():
	"""
	Captures new asset condition information and
	creates an entry in the database
	"""
	#Capture new asset category details
	if request.method == 'POST':
		condition_code = request.form['code'],
		#Check if Category code is unique
		if session.query(models.AssetCondition).filter_by(condition_code=condition_code).first():
			flash("Condition code: {} is in use by another Asset Condition".format(condition_code), "danger")
			return redirect(url_for("create_asset_condition"))

		condition_name = request.form['name']

	new_asset_condition = models.AssetCondition(
			condition_code = condition_code,
			condition_name = condition_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_condition)
	try:
		session.commit()
		flash('New asset condition; {} added successfully!'.format(condition_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to asset register
	return redirect(url_for("create_asset_condition"))

# Modify Existing Asset condition
@app.route("/asset_condition/edit_asset_condition/<condition_code>", methods=["GET"])
@login_required

def edit_asset_condition(condition_code):
	""" Provide form populated with asset condition information to be edited """

	condition = session.query(models.AssetCondition).filter(models.AssetCondition.condition_code == condition_code).all()
	condition = condition[0]

	return render_template("edit_asset_condition.html", id = condition.id,
		condition_code = condition.condition_code,
		condition_name = condition.condition_name,
		notes = condition.notes
    	)

# POST Asset condition Modifications
@app.route("/asset_condition/edit/asset_condition/<condition_code>", methods=['POST'])
@login_required

def update_asset_condition(condition_code):
	"""
	Captures updated asset condition information and
	posts updated information to the database
	"""
	condition = session.query(models.AssetCondition).filter(models.AssetCondition.condition_code == condition_code).first()
	condition.condition_code = request.form["code"]
	condition.staus_name = request.form["name"]
	condition.notes = request.form["notes"]

	session.add(condition)
	try:
		session.commit()
		flash(condition.name + ' Satus updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset condition
	return redirect(url_for("view_asset_condition"))

# Delete asset condition
@app.route("/asset_condition/delete_condition/<condition_code>")
@login_required

def condition_to_delete(condition_code):
	"""
	Identify condition to be deleted bassed on provided condition code
	"""
    #Query database for condition
	condition_search = session.query(models.AssetCondition).filter(models.AssetCondition.condition_code == condition_code).all()
	condition = [result.as_dictionary() for result in condition_search]
	condition = condition[0]

    #Display the condition details for confirmation
	return render_template("delete_condition.html", condition = condition)

# Delete asset condition from database
@app.route("/asset_condition/deleted/<condition_code>")
@login_required

def delete_asset_condition(condition_code):
	"""
	Search for confirmed asset condition and deletes it from the database
	"""
    #Search database for asset condition
	condition = session.query(models.AssetCondition).filter(models.AssetCondition.condition_code == condition_code).first()

    #Delete asset condition from database
	session.delete(condition)
	try:
		session.commit()
		flash(condition.name + ' condition deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to asset condition view
	return redirect(url_for("view_asset_condition"))


# Views to view Full list of Locations, Single Location details,
# Create New Locations, Modify Existing Location details, Delete Existing Locations

#Route to view full list of LocationsDashboard
@app.route("/location/view", methods = ["GET"])
@login_required

def view_locations():
	"""
	Queries the database for all locations and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get locations from DB
	locations_reg = session.query(models.Location).order_by(models.Location.id)

	#Convert locations_reg to a list of dictionary items
	locations_list = [location.as_dictionary() for location in locations_reg]

    #Pass dictionary list into html render function
	return render_template("view_locations.html", locations_list = locations_list)

#Single Location view route
@app.route("/location/view/<location_code>", methods = ["GET"])
@login_required

def view_location(location_code):
	"""
	Queries the database for all locations and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for location
	location_search = session.query(models.Location).filter(models.Location.location_code == location_code).all()

	#Convert result into a list of dictionary items
	location = [location.as_dictionary() for location in location_search]

	#Pass location info into html render function
	return render_template("single_location.html", location = location)

#Create new location route
@app.route("/location/add_location", methods = ["GET"])
@login_required

def create_location():
	"""	Provides empty form to be filled with new location details	"""

	return render_template("add_location.html")

@app.route("/location/add_location", methods = ["POST"])
@login_required

def add_location():
	"""
	Captures new location information and
	creates an entry in the database
	"""
	#Capture new location details
	if request.method == 'POST':
		location_code = request.form['code'],
		#Check if Location code is unique
		if session.query(models.Location).filter_by(location_code=location_code).first():
			flash("Location code: {} is in use by another Location".format(location_code), "danger")
			return redirect(url_for("create_location"))

		location_name = request.form['name']

	new_location = models.Location(
			location_code = location_code,
			location_name = location_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_location)
	try:
		session.commit()
		flash('New Location; {} added successfully!'.format(location_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to new location
	return redirect(url_for("create_location"))

# Modify Existing Location Details
@app.route("/location/edit_location/<location_code>", methods=["GET"])
@login_required

def edit_location(location_code):
	""" Provide form populated with location information to be edited """

	location = session.query(models.Location).filter(models.Location.location_code == location_code).all()
	location = location[0]

	return render_template("edit_location.html", id = location.id,
		location_code = location.location_code,
		location_name = location.location_name,
		notes = location.notes
    	)

# POST Loction Modifications
@app.route("/location/edit_location/<location_code>", methods=['POST'])
@login_required

def update_location(location_code):
	"""
	Captures updated location information and
	posts updated information to the database
	"""
	location = session.query(models.Location).filter(models.Location.location_code == location_code).first()
	location.location_code = request.form["code"]
	location.location_name = request.form["name"]
	location.notes = request.form["notes"]

	session.add(location)
	try:
		session.commit()
		flash(location.name + ' Location updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to Location view
	return redirect(url_for("view_locations"))

# Delete location
@app.route("/location/delete_location/<location_code>")
@login_required

def location_to_delete(location_code):
	"""
	Identify location to be deleted bassed on provided location code
	"""
    #Query database for location
	location_search = session.query(models.Location).filter(models.Location.location_code == location_code).all()
	location = [result.as_dictionary() for result in location_search]
	location = location[0]

    #Display the location details for confirmation
	return render_template("delete_location.html", location = location)

# Delete location from database
@app.route("/location/deleted/<location_code>")
@login_required

def delete_location(location_code):
	"""
	Search for confirmed location and deletes it from the database
	"""
    #Search database for location
	location = session.query(models.Location).filter(models.Location.location_code == location_code).first()

    #Delete location from database
	session.delete(location)
	try:
		session.commit()
		flash(location.name + ' Location deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to locations view
	return redirect(url_for("view_locations"))


# Views to view Full list of Cost Centers, Single Cost Center details,
# Create New Cost Center, Modify Existing Cost Center details, Delete Existing Cost Centers

#Route to view full list of Cost Centers
@app.route("/cost_centers/view", methods = ["GET"])
@login_required

def view_costcenters():
	"""
	Queries the database for all cost centers and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get cost centers from DB
	costcenters_reg = session.query(models.CostCenter).order_by(models.CostCenter.id)

	#Convert costcenters_reg to a list of dictionary items
	costcenters_list = [costcenter.as_dictionary() for costcenter in costcenters_reg]

    #Pass dictionary list into html render function
	return render_template("view_cost_centers.html", costcenters_list = costcenters_list)

#Single Cost Center view route
@app.route("/cost_center/view/<center_code>", methods = ["GET"])
@login_required

def view_costcenter(center_code):
	"""
	Queries the database for all cost centers and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for cost centers
	costcenter_search = session.query(models.CostCenter).filter(models.CostCenter.center_code == center_code).all()

	#Convert result into a list of dictionary items
	costcenter = [costcenter.as_dictionary() for costcenter in costcenter_search]

	#Pass cost center info into html render function
	return render_template("single_costcenter.html", costcenter = costcenter)

#Create new Cost Center route
@app.route("/cost_center/add_cost_center", methods = ["GET"])
@login_required

def create_costcenter():
	"""	Provides empty form to be filled with new cost center details	"""

	return render_template("add_costcenter.html")

@app.route("/cost_center/add_cost_center", methods = ["POST"])
@login_required

def add_costcenter():
	"""
	Captures new cost center information and
	creates an entry in the database
	"""
	#Capture new cost center details
	if request.method == 'POST':
		center_code = request.form['code'],
		#Check if Center code is unique
		if session.query(models.CostCenter).filter_by(center_code=center_code).first():
			flash("Center code: {} is in use by another CostCenter".format(category_code), "danger")
			return redirect(url_for("create_costcenter"))

		center_name = request.form['name']

	new_costcenter = models.CostCenter(
			center_code = center_code,
			center_name = center_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_costcenter)
	try:
		session.commit()
		flash('New cost center; {} added successfully!'.format(center_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to new cost center
	return redirect(url_for("create_costcenter"))

# Modify Existing Cost Center Details
@app.route("/cost_center/edit_cost_center/<center_code>", methods=["GET"])
@login_required

def edit_costcenter(center_code):
	""" Provide form populated with cost center information to be edited """

	costcenter = session.query(models.CostCenter).filter(models.CostCenter.center_code == center_code).all()
	costcenter = costcenter[0]

	return render_template("edit_costcenter.html", id = costcenter.id,
		center_code = costcenter.center_code,
		center_name = costcenter.center_name,
		notes = costcenter.notes
    	)

# POST Cost Center Modifications
@app.route("/cost_center/edit_cost_center/<center_code>", methods=['POST'])
@login_required

def update_costcenter(center_code):
	"""
	Captures updated cost center information and
	posts updated information to the database
	"""
	costcenter = session.query(models.CostCenter).filter(models.CostCenter.center_code == center_code).first()
	costcenter.center_code = request.form["code"]
	costcenter.center_name = request.form["name"]
	costcenter.notes = request.form["notes"]

	session.add(costcenter)
	try:
		session.commit()
		flash(costcenter.name + ' Cost Center updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to Cost Centers view
	return redirect(url_for("view_costcenters"))

# Delete Cost Center
@app.route("/cost_center/delete_cost_center/<center_code>")
@login_required

def costcenter_to_delete(center_code):
	"""
	Identify cost center to be deleted bassed on provided center code
	"""
    #Query database for cost center
	costcenter_search = session.query(models.CostCenter).filter(models.CostCenter.center_code == center_code).all()
	costcenter = [result.as_dictionary() for result in costcenter_search]
	costcenter = costcenter[0]

    #Display the cost center details for confirmation
	return render_template("delete_costcenter.html", costcenter = costcenter)

# Delete cost center from database
@app.route("/cost_center/deleted/<center_code>")
@login_required

def delete_costcenter(center_code):
	"""
	Search for confirmed cost center and deletes it from the database
	"""
    #Search database for cost center
	costcenter = session.query(models.CostCenter).filter(models.CostCenter.center_code == center_code).first()

    #Delete cost center from database
	session.delete(costcenter)
	try:
		session.commit()
		flash(costcenter.name + ' Cost Center deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to cost centers view
	return redirect(url_for("view_costcenters"))


# Views to view Full list of Departments, Single Department details,
# Create New Departments, Modify Existing Departments details, Delete Existing Departments

#Route to view full list of Departments
@app.route("/departments/view", methods = ["GET"])
@login_required

def view_departments():
	"""
	Queries the database for all departments and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get Departments from DB
	departments_reg = session.query(models.Department).order_by(models.Department.id)

	#Convert departments_reg to a list of dictionary items
	departments_list = [department.as_dictionary() for department in departments_reg]

    #Pass dictionary list into html render function
	return render_template("view_departments.html", departments_list = departments_list)

#Single department view route
@app.route("/department/view/<department_code>", methods = ["GET"])
@login_required

def view_department(department_code):
	"""
	Queries the database for all departments and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for departments
	department_search = session.query(models.Department).filter(models.Department.department_code == department_code).all()

	#Convert result into a list of dictionary items
	department = [department.as_dictionary() for department in department_search]

	#Pass departments info into html render function
	return render_template("single_department.html", department = department)

#Create new Department route
@app.route("/department/add_department", methods = ["GET"])
@login_required

def create_department():
	"""	Provides empty form to be filled with new department details	"""

	return render_template("add_department.html")

@app.route("/department/add_department", methods = ["POST"])
@login_required

def add_department():
	"""
	Captures new departments information and
	creates an entry in the database
	"""
	#Capture new departments details
	if request.method == 'POST':
		department_code = request.form['code'],
		#Check if Department code is unique
		if session.query(models.Department).filter_by(department_code=department_code).first():
			flash("Department code: {} is in use by another Department".format(department_code), "danger")
			return redirect(url_for("create_asset_category"))

		department_name = request.form['name']

	new_department = models.Department(
			department_code = department_code,
			department_name = department_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_department)
	try:
		session.commit()
		flash('New department; {} added successfully!'.format(department_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to new departments
	return redirect(url_for("create_department"))

# Modify Existing Department Details
@app.route("/department/edit_department/<department_code>", methods=["GET"])
@login_required

def edit_department(department_code):
	""" Provide form populated with department information to be edited """

	department = session.query(models.Department).filter(models.Department.department_code == department_code).all()
	department = department[0]

	return render_template("edit_departments.html", id = department.id,
		department_code = department.department_code,
		department_name = department.department_name,
		notes = department.notes
    	)

# POST Department Modifications
@app.route("/department/edit_department/<department_code>", methods=['POST'])
@login_required

def update_department(department_code):
	"""
	Captures updated department information and
	posts updated information to the database
	"""
	department = session.query(models.Department).filter(models.Department.department_code == department_code).first()
	department.department_code = request.form["code"]
	department.department_name = request.form["name"]
	department.notes = request.form["notes"]

	session.add(department)
	try:
		session.commit()
		flash(department.name + ' department updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to Departments view
	return redirect(url_for("view_departments"))

# Delete Department
@app.route("/department/delete_department/<department_code>")
@login_required

def department_to_delete(department_code):
	"""
	Identify department to be deleted bassed on provided department code
	"""
    #Query database for department
	department_search = session.query(models.Department).filter(models.Department.department_code == department_code).all()
	department = [result.as_dictionary() for result in department_search]
	department = department[0]

    #Display the department details for confirmation
	return render_template("delete_department.html", department = department)

# Delete department from database
@app.route("/department/deleted/<department_code>")
@login_required

def delete_department(department_code):
	"""
	Search for confirmed department and deletes it from the database
	"""
    #Search database for department
	department = session.query(models.Department).filter(models.Department.department_code == department_code).first()

    #Delete department from database
	session.delete(department)
	try:
		session.commit()
		flash(department.name + ' department deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to departments view
	return redirect(url_for("view_departments"))


# Views to view Full list of People, Single People details,
# Create New People, Modify Existing Person details, Delete Existing People

#Route to view full list of People
@app.route("/people/view", methods = ["GET"])
@login_required

def view_people():
	"""
	Queries the database for all people and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get People from DB
	people_reg = session.query(models.People).order_by(models.People.id)

	#Convert people_reg to a list of dictionary items
	people_list = [person.as_dictionary() for person in people_reg]

    #Pass dictionary list into html render function
	return render_template("view_people.html", people_list = people_list)

#Single person view route
@app.route("/person/view/<person_code>", methods = ["GET"])
@login_required

def view_person(person_code):
	"""
	Queries the database for all people and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for person
	person_search = session.query(models.People).filter(models.People.person_code == person_code).all()

	#Convert result into a list of dictionary items
	person = [person.as_dictionary() for person in person_search]

	#Pass person info into html render function
	return render_template("single_person.html", person = person)

#Create new Person route
@app.route("/people/add_person", methods = ["GET"])
@login_required

def create_person():
	"""	Provides empty form to be filled with new person details """

	#Get departments from DB
	departments_list = session.query(models.Department).order_by(models.Department.department_code)

	#Get locations from DB
	locations_list = session.query(models.Location).order_by(models.Location.location_code)

	return render_template("add_person.html", departments_list = departments_list,
							locations_list = locations_list
							)

@app.route("/people/add_person", methods = ["POST"])
@login_required

def add_person():
	"""
	Captures new person information and
	creates an entry in the database
	"""
	#Capture new person details
	if request.method == 'POST':
		person_code = request.form['code']
		if session.query(models.People).filter_by(person_code=person_code).first():
			flash("Person with code: {} already exists".format(person_code), "danger")
			return redirect(url_for("create_person"))
		email = request.form['email']
		if session.query(models.People).filter_by(email=email).first():
			flash("Person with email: {} already exists".format(email), "danger")
			return redirect(url_for("create_person"))
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		designation = request.form['designation']
		phone = request.form['phone']
		department_id = request.form['department']
		location_id = request.form['location']
		notes = request.form["notes"]

	new_person = models.People(person_code = person_code, first_name = first_name,
								last_name = last_name, designation = designation,
								phone = phone, email = email, department_id = department_id,
								location_id = location_id, notes = notes
								)
	#Add entry to database
	session.add(new_person)
	try:
		session.commit()
		flash('{} {} has been added successfully!'.format(first_name, last_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to new person
	return redirect(url_for("create_person"))

# Modify Existing Person Details
@app.route("/people/edit_person/<person_code>", methods=["GET"])
@login_required

def edit_person(person_code):
	""" Provide form populated with person information to be edited """

	person = session.query(models.People).filter(models.People.person_code == person_code).all()
	person = person[0]

	return render_template("edit_person.html", id = person.id,
		person_code = person.person_code,
		first_name = person.first_name,
		last_name = person.last_name,
		designation = person.designation,
		phone = person.phone,
		email = person.email,
		department = person.department,
		location = person.location,
		notes = person.notes
    	)

# POST Person Modifications
@app.route("/people/edit_person/<person_code>", methods=['POST'])
@login_required

def update_person(person_code):
	"""
	Captures updated person information and
	posts updated information to the database
	"""
	person = session.query(models.People).filter(models.People.person_code == person_code).first()
	person.person_code = request.form["code"]
	person.first_name = request.form["first_name"]
	person.last_name = request.form["last_name"]
	person.designation = request.form["designation"]
	person.phone = request.form["phone"]
	person.email = request.form["email"]
	person.department = request.form["department"]
	person.location = request.form["location"]
	person.notes = request.form["notes"]

	session.add(person)
	try:
		session.commit()
		flash(person.first_name + ' ' + person.last_name + " record updated successfully.", category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to People view
	return redirect(url_for("view_people"))

# Delete Person
@app.route("/people/delete_person/<person_code>")
@login_required

def person_to_delete(person_code):
	"""
	Identify person to be deleted bassed on provided person's code
	"""
    #Query database for person
	person_search = session.query(models.People).filter(models.People.person_code == person_code).all()
	person = [result.as_dictionary() for result in person_search]
	person = person[0]

    #Display the person details for confirmation
	return render_template("delete_person.html", person = person)

# Delete person from database
@app.route("/people/deleted/<person_code>")
@login_required

def delete_person(person_code):
	"""
	Search for confirmed person and deletes it from the database
	"""
    #Search database for person
	person = session.query(models.People).filter(models.People.person_code == person_code).first()

    #Delete person from database
	session.delete(person)
	try:
		session.commit()
		flash(person.first_name + ' '  + person.last_name + ' deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to people view
	return redirect(url_for("view_people"))


# Views to view Full list of Supplier Categories, Single Supplier Category details,
# Create New Supplier Category, Modify Existing Supplier Category details,
# Delete Existing Supplier Category

#Route to view full list of Supplier Category
@app.route("/supplier_categories/view", methods = ["GET"])
@login_required

def view_supplierCategories():
	"""
	Queries the database for all supplier categories and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get Supplier Categories from DB
	supplierCategories_reg = session.query(models.SupplierCategory).order_by(models.SupplierCategory.id)

	#Convert supplierCategories_reg to a list of dictionary items
	supplierCategories_list = [supplierCategory.as_dictionary() for supplierCategory in supplierCategories_reg]

    #Pass Supplier Categories list into html render function
	return render_template("view_supplier_categories.html", supplierCategories_list = supplierCategories_list)

#Single supplier category view route
@app.route("/supplier_category/view/<category_code>", methods = ["GET"])
@login_required

def view_supplierCategory(category_code):
	"""
	Queries the database for all supplier category and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for supplier category
	supplierCategory_search = session.query(models.SupplierCategory).filter(models.SupplierCategory.category_code == category_code).all()

	#Convert result into a list of dictionary items
	supplierCategory = [supplierCategory.as_dictionary() for supplierCategory in supplierCategory_search]

	#Pass supplier category info into html render function
	return render_template("single_supplier_category.html", supplierCategory = supplierCategory)

#Create new Supplier Category route
@app.route("/supplier_categories/add_supplier_category", methods = ["GET"])
@login_required

def create_supplierCategory():
	"""	Provides empty form to be filled with new supplier category details	"""

	return render_template("add_suppliercategory.html")

@app.route("/supplier_categories/add_supplier_category", methods = ["POST"])
@login_required

def add_supplierCategory():
	"""
	Captures new supplier category information and
	creates an entry in the database
	"""
	#Capture new supplier category details
	if request.method == 'POST':
		category_code = request.form['code'],
		#Check if Category code is unique
		if session.query(models.AssetCategory).filter_by(category_code=category_code).first():
			flash("Category code: {} is in use by another Supplier Category".format(category_code), "danger")
			return redirect(url_for("create_supplierCategory"))

		category_name = request.form['name']

	new_supplierCategory = models.SupplierCategory(
			category_code = category_code,
			category_name = category_name,
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_supplierCategory)
	try:
		session.commit()
		flash('New supplier category; {} has been added successfully!'.format(category_name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to create new supplier
	return redirect(url_for("create_supplierCategory"))

# Modify Existing Supplier Category Details
@app.route("/supplier_category/edit_category/<category_code>", methods=["GET"])
@login_required

def edit_supplierCategory(category_code):
	""" Provide form populated with supplier categories information to be edited """

	supplierCategory = session.query(models.SupplierCategory).filter(models.SupplierCategory.category_code == category_code).all()
	supplierCategory = supplierCategory[0]

	return render_template("edit_supplier_category.html", id = supplierCategory.id,
		category_code = supplierCategory.category_code,
		category_name = supplierCategory.category_name,
		notes = supplierCategory.notes
    	)

# POST Supplier Category Modifications
@app.route("/supplier_category/edit_category/<category_code>", methods=['POST'])
@login_required

def update_supplierCategory(category_code):
	"""
	Captures updated supplier category information and
	posts updated information to the database
	"""
	supplierCategory = session.query(models.SupplierCategory).filter(models.SupplierCategory.category_code == category_code).first()
	supplierCategory.category_code = request.form["code"]
	supplierCategory.category_name = request.form["name"]
	supplierCategory.notes = request.form["notes"]

	session.add(supplierCategory)
	try:
		session.commit()
		flash('Supplier Category updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to Supplier Categories view
	return redirect(url_for("view_supplierCategories"))

# Delete Supplier Category
@app.route("/supplier_category/delete_category/<category_code>")
@login_required

def supplierCategory_to_delete(category_code):
	"""
	Identify supplier category to be deleted bassed on provided supplier category code
	"""
    #Query database for supplier category
	supplierCategory_search = session.query(models.SupplierCategory).filter(models.SupplierCategory.category_code == category_code).all()
	supplierCategory = [result.as_dictionary() for result in supplierCategory_search]
	supplierCategory = supplierCategory[0]

    #Display the supplier category details for confirmation
	return render_template("delete_supplier_category.html", supplierCategory = supplierCategory)

# Delete supplier from database
@app.route("/supplier_category/deleted/<category_code>")
@login_required

def delete_supplierCategory(category_code):
	"""
	Search for confirmed supplier category and deletes it from the database
	"""
    #Search database for supplier category
	supplierCategory = session.query(models.SupplierCategory).filter(models.SupplierCategory.category_code == category_code).first()

    #Delete supplier category from database
	session.delete(supplierCategory)
	try:
		session.commit()
		flash('Supplier Category successfully deleted.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to supplier categories view
	return redirect(url_for("view_supplierCategories"))


# Views to view Full list of Supplier, Single Supplier details,
# Create New Supplier, Modify Existing Supplier details, Delete Existing Supplier

#Route to view full list of Supplier
@app.route("/suppliers/view", methods = ["GET"])
@login_required

def view_suppliers():
	"""
	Queries the database for all suppliers and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
    #Get Suppliers from DB
	suppliers_reg = session.query(models.Supplier).order_by(models.Supplier.id)

	#Convert suppliers_reg to a list of dictionary items
	suppliers_list = [supplier.as_dictionary() for supplier in suppliers_reg]

    #Pass dictionary list into html render function
	return render_template("view_suppliers.html", suppliers_list = suppliers_list)

#Single Supplier view route
@app.route("/supplier/view/<supplier_code>", methods = ["GET"])
@login_required

def view_supplier(supplier_code):
	"""
	Queries the database for all supplier and passes them into a
	list of dictionaries which is passed into the hmtl render
	function
	"""
	#Search for supplier
	supplier_search = session.query(models.Supplier).filter(models.Supplier.supplier_code == supplier_code).all()

	#Convert result into a list of dictionary items
	supplier = [supplier.as_dictionary() for supplier in supplier_search]

	#Pass supplier info into html render function
	return render_template("single_supplier.html", supplier = supplier)

#Create new Supplier route
@app.route("/suppliers/add_supplier", methods = ["GET"])
@login_required

def create_supplier():
	"""	Provides empty form to be filled with new supplier details	"""

	#Get supplier category from DB
	categories_list = session.query(models.SupplierCategory).order_by(models.SupplierCategory.category_code)

	#Get locations from DB
	locations_list = session.query(models.Location).order_by(models.Location.location_code)

	#Get contact person from DB
	contacts_list = session.query(models.People).order_by(models.People.person_code)

	return render_template("add_supplier.html", categories_list = categories_list,
							locations_list = locations_list, contacts_list = contacts_list
							)

@app.route("/suppliers/add_supplier", methods = ["POST"])
@login_required

def add_supplier():
	"""
	Captures new supplier information and creates an entry in the database
	"""
	#Capture new supplier details
	if request.method == 'POST':
		code = request.form['code'],
		#Check if Supplier code is unique
		if session.query(models.Supplier).filter_by(code=code).first():
			flash("Supplier code: {} is in use by another Supplier".format(code), "danger")
			return redirect(url_for("create_supplier"))

		name = request.form['name']

	new_supplier = models.Supplier(
			code = code,
			name = name,
			phone = request.form['phone'],
			email = request.form['email'],
			website = request.form['website'],
			category_id = request.form['category'],
			location_id = request.form['location'],
			contact_person = request.form['contact_person'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_supplier)
	try:
		session.commit()
		flash('New supplier; {} added successfully!'.format(name), 'success')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', 'danger')
		session.rollback
		raise error
	finally:
		session.close()

	#Return to new supplier
	return redirect(url_for("create_supplier"))

# Modify Existing Supplier Details
@app.route("/supplier/edit_supplier/<supplier_code>", methods=["GET"])
@login_required

def edit_supplier(supplier_code):
	""" Provide form populated with supplier information to be edited """

	supplier = session.query(models.Supplier).filter(models.Supplier.supplier_code == supplier_code).all()
	supplier = supplier[0]

	return render_template("edit_supplier.html", id = supplier.id,
		supplier_code = supplier.supplier_code,
		supplier_name = supplier.supplier_name,
		phone = supplier.phone,
		email = supplier.email,
		website = supplier.website,
		category = supplier.category,
		location = supplier.location,
		contact_person = supplier.contact_person,
		notes = supplier.notes
    	)

# POST Person Modifications
@app.route("/supplier/edit_supplier/<supplier_code>", methods=['POST'])
@login_required

def update_supplier(supplier_code):
	"""
	Captures updated supplier information and posts updated information to the database
	"""
	supplier = session.query(models.Supplier).filter(models.Supplier.supplier_code == supplier_code).first()
	supplier.supplier_code = request.form["code"]
	supplier.supplier_name = request.form["name"]
	supplier.phone = request.form["phone"]
	supplier.email = request.form["email"]
	supplier.website = request.form["website"]
	supplier.location = request.form["location"]
	supplier.contact_person = request.form["contact_person"]
	supplier.notes = request.form["notes"]

	session.add(supplier)
	try:
		session.commit()
		flash('Supplier details have been updated successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to Supplier view
	return redirect(url_for("view_suppliers"))

# Delete Supplier
@app.route("/supplier/delete_supplier/<supplier_code>")
@login_required

def supplier_to_delete(supplier_code):
	"""
	Identify supplier to be deleted bassed on provided supplier's code
	"""
    #Query database for supplier
	supplier_search = session.query(models.Supplier).filter(models.Supplier.supplier_code == supplier_code).all()
	supplier = [result.as_dictionary() for result in supplier_search]
	supplier = supplier[0]

    #Display the supplier details for confirmation
	return render_template("delete_supplier.html", supplier = supplier)

# Delete supplier from database
@app.route("/supplier/deleted/<supplier_code>")
@login_required

def delete_supplier(supplier_code):
	"""
	Search for confirmed supplier and deletes it from the database
	"""
    #Search database for supplier
	supplier = session.query(models.Supplier).filter(models.Supplier.supplier_code == supplier_code).first()

    #Delete supplier from database
	session.delete(supplier)
	try:
		session.commit()
		flash(supplier.name + ' Supplier deleted successfully.', category='message')
	except SQLAlchemyError as error:
		flash('Something went wrong, please make sure your information is correct.', category='error')
		session.rollback
		raise error
	finally:
		session.close()

    #Return to suppliers view
	return redirect(url_for("view_suppliers"))