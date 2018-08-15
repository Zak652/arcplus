from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, LoginManager, logout_user
from flask_bootstrap import Bootstrap

from flask import flash
from getpass import getpass
from werkzeug.security import generate_password_hash, check_password_hash

from . import app, decorators, models
from .database import session


# Start route and Authentication

#Appliction requires login from the start
@app.route("/")
def index():
	""" Application requires users to login first.
		All initial access is redirected to login page.
	"""
    # Redirect user to login page
	return redirect(url_for("login_get"))


# Views for Adding New Users, Users Login and Logout

# New User registration. Get user information
@app.route("/user/registration", methods = ["GET"])
def add_user():
	""" Display user registration form """

	return render_template("add_user.html")

# Verify user information and register new user 
@app.route("/user/registration", methods = ["POST"])
def new_user():

	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		#check if email is unique / doesn't exist already
		if session.query(models.User).filter_by(email=email).first():
			flash("User with that email address already exists", "danger")
			return
		password = request.form['password']
		#Check if password is not less than 8 characters
		if len(password) < 8:
			flash("Password should be 8 or more characters long")
			return

	# Add users to DB
	new_user = models.User(name=name, email = email, password = generate_password_hash(password))
	session.add(new_user)
	session.commit()
	return redirect(url_for("login_get"))

# User Login Access
@app.route("/user/login", methods=["GET"])
def login_get():
	""" Provide login form and collect login credentials """
	return render_template("login.html")

# Verify user credentials provided on login form
@app.route("/user/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(models.User).filter_by(email = email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(url_for("view_register"))

#Logout User
@app.route("/user/logout")
def logout():
	logout_user()
	return redirect(url_for("login_get"))


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
	return render_template("asset_register.html", assets = assets)

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

	return render_template("add_asset.html")

# Post New Asset information
@app.route("/register/add_asset", methods = ["POST"])
@login_required
def add_asset():
	"""
	Captures new asset information and 
	creates an entry in the database
	"""
	#Capture new asset details
	new_asset = models.Asset(
			barcode = request.form['barcode'],
			serial_no = request.form['serial_no'],
			name = request.form['name'],
			category = request.form['category'],
			_type = request.form['_type'],
			_model = request.form['_model'],
			status = request.form['status'],
			location = request.form['location'],
			cost_center = request.form['cost_center'],
			user = request.form['user'],
			purchase_price = request.form['purchase_price'],
			supplier = request.form['supplier'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_register"))

# Modify Existing Asset
@app.route("/register/edit/asset/<barcode>", methods=["GET"])
@login_required
def edit_asset(barcode):
	""" Provide form populated with asset information to be edited """

	asset = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()
	asset = asset[0]

	return render_template("edit_asset.html", id = asset.id,
		barcode = asset.barcode, serial_no = asset.serial_no,
    	name = asset.name, category = asset.category, _type = asset._type,
    	_model = asset._model, status = asset.status, location = asset.location,
    	cost_center = asset.cost_center, user = asset.user, supplier = asset.supplier, 
		purchase_price = asset.purchase_price, notes = asset.notes
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
		except(ValueError):
			sent = 0

	asset.value = sent
	asset.supplier = request.form["supplier"]
	asset.photo = request.form["photo"]
	asset.notes = request.form["notes"]

	session.add(asset)
	session.commit()

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
	session.commit()

    #Return to asset register
	return redirect(url_for("view_register"))


# Views to view Full list of Asset Categories, Single Asset Category,
# Create New Category, Modify Existing Category details, Delete Existing Category

#Route to view full list of asset categories
@app.route("/asset_categories/view", methods = ["GET"])
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
	return render_template("asset_categories.html", category_list = category_list)

#Single Asset Category view route
@app.route("/asset_categories/view/<category_code>", methods = ["GET"])
def view_single_category(category_code):
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
def create_asset_category():
	"""	Provides empty form to be filled with new asset category details	"""

	return render_template("add_asset_category.html")

@app.route("/asset_categories/add_asset_category", methods = ["POST"])
def add_asset_category():
	"""
	Captures new asset category information and 
	creates an entry in the database
	"""
	#Capture new asset category details
	new_asset_category = models.AssetCategory(
			category_code = request.form['code'],
			category_name = request.form['name'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_category)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_asset_categories"))

# Modify Existing Asset Category
@app.route("/asset_categories/edit/asset_category/<category_code>", methods=["GET"])
@login_required
def edit_asset_category(category_code):
	""" Provide form populated with asset category information to be edited """

	category = session.query(models.AssetCategory).filter(models.AssetCategory.category_code == category_code).all()
	category = category[0]

	return render_template("edit_asset_category.html", id = category.id,
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
	session.commit()

    #Return to asset register
	return redirect(url_for("view_asset_categories"))


# Views to view Full list of Asset Types, Single Asset Type,
# Create New Type, Modify Existing Type details, Delete Existing Type

#Route to view full list of asset types
@app.route("/asset_types/view", methods = ["GET"])
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
	return render_template("asset_types.html", types_list = types_list)

#Single Asset type view route
@app.route("/asset_types/view/<type_code>", methods = ["GET"])
def view_single_type(type_code):
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
def create_asset_type():
	"""	Provides empty form to be filled with new asset type details	"""

	return render_template("add_asset_type.html")

@app.route("/asset_types/add_asset_type", methods = ["POST"])
def add_asset_type():
	"""
	Captures new asset type information and 
	creates an entry in the database
	"""
	#Capture new asset type details
	new_asset_type = models.AssetType(
			type_code = request.form['code'],
			type_name = request.form['name'],
			type_category = request.form['category'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_type)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_asset_types"))

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
	session.commit()

    #Return to asset types
	return redirect(url_for("view_asset_types"))


# Views to view Full list of Asset Models, Single Asset Model,
# Create New Model, Modify Existing Model details, Delete Existing Model

#Route to view full list of asset models
@app.route("/asset_models/view", methods = ["GET"])
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
	return render_template("asset_models.html", models_list = models_list)

#Single Asset model view route
@app.route("/asset_models/view/<model_code>", methods = ["GET"])
def view_single_model(model_code):
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
def create_asset_model():
	"""	Provides empty form to be filled with new asset model details	"""

	return render_template("add_asset_model.html")

@app.route("/asset_models/add_asset_model", methods = ["POST"])
def add_asset_model():
	"""
	Captures new asset model information and 
	creates an entry in the database
	"""
	#Capture new asset category details
	new_asset_model = models.AssetModel(
			model_code = request.form['code'],
			model_name = request.form['name'],
			model_type = request.form['model_type'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_model)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_asset_models"))

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
	session.commit()

    #Return to asset models
	return redirect(url_for("view_asset_models"))


# Views to view Full list of Asset Status, Single Asset Status,
# Create New Status, Modify Existing Status details, Delete Existing Status

#Route to view full list of asset Status
@app.route("/asset_Status/view", methods = ["GET"])
def view_asset_status():
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
	return render_template("asset_status.html", status_list = status_list)

#Single Asset status view route
@app.route("/asset_status/view/<status_code>", methods = ["GET"])
def view_single_status(status_code):
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
	return render_template("single_status.html", staus = status)

#Create new asset model route
@app.route("/asset_status/add_asset_status", methods = ["GET"])
def create_asset_status():
	"""	Provides empty form to be filled with new asset status details	"""

	return render_template("add_asset_status.html")

@app.route("/asset_status/add_asset_status", methods = ["POST"])
def add_asset_status():
	"""
	Captures new asset status information and 
	creates an entry in the database
	"""
	#Capture new asset category details
	new_asset_status = models.AssetStatus(
			status_code = request.form['code'],
			status_name = request.form['name'],
			status_type = request.form['status_type'],
			notes = request.form["notes"]
			)
	#Add entry to database
	session.add(new_asset_status)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_asset_status"))

# Modify Existing Asset Status
@app.route("/asset_status/edit/asset_status/<status_code>", methods=["GET"])
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
	session.commit()

    #Return to asset status
	return redirect(url_for("view_asset_status"))