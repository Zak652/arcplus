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


# Routes for Adding New Users, Users Login and Logout

# New User registration. Get user information
@app.route("/user/registration", methods = ["GET"])
def add_user():
	""" Display user registration form """

	return render_template("add_user.html")

# Verify user information and register new user 
@app.route("/user/registration", methods = ["POST"])
def new_user():

	name = request.form['name']
	email = request.form['email']
	# email should be unique, check if it exists
	if session.query(models.User).filter_by(email=email).first():
		flash("User with that email address already exists", "danger")
		return
	# Password needs to be 8 characters or more
	password = request.form['password']
	if len(password) < 8:
		flash("Password should be 8 or more characters long")
		return
	# Add users to DB
	user = models.User(name=name, email = email, password = generate_password_hash(password))
	session.add(user)
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


# Routes for Viewing full asset register, Single asset, Creating New Asset,
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
	creates add entry in the database
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
			user = request.form['user'],
			purchase_price = request.form['purchase_price'],
			supplier = request.form['supplier'],
			comments = request.form["comments"]
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
    	user = asset.user, purchase_price = asset.purchase_price,
    	supplier = asset.supplier, comments = asset.comments
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
	asset.comments = request.form["comments"]

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


# Routes to view Full list of Asset Categories, Single Asset Category,
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
	return render_template("asset_register.html", category_list = category_list)

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
	creates add entry in the database
	"""
	#Capture new asset category details
	new_asset_category = models.AssetCategory(
			category_code = request.form['barcode'],
			category_name = request.form['name'],
			comments = request.form["comments"]
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
		comments = category.comments
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
	category.comments = request.form["comments"]

	session.add(category)
	session.commit()

    #Return to asset register
	return redirect(url_for("view_asset_categories"))