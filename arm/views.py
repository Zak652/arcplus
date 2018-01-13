from flask import render_template, request, redirect, url_for, flash

from . import app, decorators, models
from .database import session


#Appliction landing page
@app.route("/")
def index():
    return render_template("index.html")


#Full Register view route
@app.route("/register/view", methods = ["GET"])
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


#Single asset view route
@app.route("/register/view/<barcode>", methods = ["GET"])
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


#Create new asset route
@app.route("/register/add_asset", methods = ["GET"])
def create_asset():
	"""	Provides empty form to be filled with asset details	"""

	return render_template("add_asset.html")

@app.route("/register/add_asset", methods = ["POST"])
def add_asset():
	"""
	Captures new asset information and 
	creates add entry in the database
	"""
	#Capture new asset details
	new_asset = models.Asset(
			barcode = request.form['barcode'],
			serial_no = request.form['serial'],
			name = request.form['name'],
			category = request.form['category'],
			_type = request.form['_type'],
			_model = request.form['_model'],
			status = request.form['status'],
			location = request.form['location'],
			user = request.form['user'],
			purchase_price = request.form['price'],
			supplier = request.form['supplier'],
			comments = request.form["comments"]
			)
	#Add entry to database
	session.add(new_asset)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_register"))


#Modify Existing Asset
@app.route("/register/edit/<barcode>", methods=["GET"])
def edit_asset(barcode):
	""" Provide form populated with asset information to be edited """

	asset = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()
	asset = asset[0]

	return render_template("edit_asset.html", 
		barcode = asset.barcode, serial_no = asset.serial_no,
    	name = asset.name, category = asset.category, _type = asset._type,
    	_model = asset._model, status = asset.status, location = asset.location,
    	user = asset.user, purchase_price = asset.purchase_price,
    	supplier = asset.supplier, comments = asset.comments
    	)

@app.route("/register/edit/<barcode>", methods=['POST'])
def update_asset(barcode):
	"""
	Captures updated asset information and 
	posts updated information to the database
	"""
	#Capture updates from asset form
	asset_update = models.Asset(
    		id = id,
    		barcode = request.form["barcode"],
    		serial_no = request.form["serial_no"],
    		name = request.form["name"],
    		category = request.form["category"],
    		_type = request.form["_type"],
    		_model = request.form["_model"],
    		status = request.form["status"],
    		location = request.form["location"],
    		user = request.form["user"],
    		purchase_price = request.form["purchase_price"],
    		supplier = request.form["supplier"],
    		comments = request.form["comments"]
    		)
    #Merge updates with asset entry
	session.merge(asset_update)
	session.commit()

    #Return to asset register
	return redirect(url_for("view_register"))

#Delete asset from register
@app.route("/register/delete/<barcode>")
def asset_to_delete(barcode):
	"""
	Identify asset to be deleted bassed on provided barcode
	"""
    #Query database for asset
	asset_search = session.query(models.Asset).filter(models.Asset.barcode == barcode).all()
	asset = [result.as_dictionary() for result in asset_search]

    #Display the asset details for confirmation
	return render_template("delete_asset.html", asset = asset)

@app.route("/register/delete/<barcode>")
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