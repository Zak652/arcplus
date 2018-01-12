from flask import render_template, request, redirect, url_for

from . import app, decorators, models
from .database import session

#Appliction landing page
@app.route("/")
def index():
    return render_template("index.html")

#Full Register view route
@app.route("/register", methods = ["GET"])
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
@app.route("/register/<barcode>", methods = ["GET"])
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
@app.route("/add_asset", methods = ["GET"])
def get_new_asset():
	"""	Provides empty form to be filled with asset details	"""

	return render_template("add_asset.html")

@app.route("/add_asset", methods = ["POST"])
def add_new_asset():
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
			supplier = request.form['supplier']
			)
	#Add entry to database
	session.add(new_asset)
	session.commit()

	#Return to asset register
	return redirect(url_for("view_register"))