import os.path
import json

from flask import Flask, Response, send_from_directory

# solves most responses you need
from flask import render_template, request, redirect, url_for, flash

# if authentication is needed, this is where you start
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import check_password_hash

#Required File upload security
from werkzeug.utils import secure_filename

#Required for JSON Validation
from jsonschema import validate, ValidationError

from . import app, decorators, models
from .database import session


#Get register to display
@app.route("/api/register", methods = ["GET"])
@decorators.accept("application/json")
def asset_register():

    #Get assets from DB
	assets = session.query(models.Asset).order_by(models.Asset.id)

	#Converts assets to Json and returns the appropriate response
	data = json.dumps([asset.as_dictionary() for asset in assets], indent=4, sort_keys=False, default=str)

    #Return response and render html
	return Response(data, 200, mimetype="application/json"), render_template("asset_register.html", data = data)

#Single asset view based on asset barcode
@app.route("/api/register/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def get_asset(barcode):
    """ Single asset view endpoint """
    
    #Finds asset from database using Barcode number
    asset = session.query(models.Asset).get(barcode)
    
    #First confirm existance of asset in database
    if not asset:
        message = "Could not find asset with barcode number {}".format(barcode)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype = "application/json")
        
    #Returns post as JSON
    data = json.dumps(asset.as_dictionary(), indent=4, sort_keys=True, default=str)
    return Response(data, 200, mimetype="application/json")

#Route for collecting new assets information
@app.route("/api/add_asset", methods=["GET"])
@decorators.accept("application/json")
def new_asset_data():
	""" Provides form to be filled with new asset data """

	return render_template("add_asset.html")


#Route for posting asset info to database
@app.route("/api/add_asset", methods = ["POST"])
@decorators.accept("application/json")
def add_asset():
	""" Create New Asset """

	#Capture data from new asset form
	asset = models.Asset(
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
    #Create new asset in database
	session.add(asset)
	session.commit()

	#Confirm new asset has been addded to database
	new_asset = session.query(models.Asset).get(asset.barcode)

	if not new_asset:
		message = "ERROR: Asset with barcode number {} has not been addded".format(asset.barcode)
		data = json.dumps({"message": message})
		return Response(data, 404, mimetype = "application/json")

    #Conver new asset data to Json and return confimation message
	data = json.dumps([new_asset.as_dictionary()], indent=4, sort_keys=True, default=str)
	return Response(data, 200, mimetype="application/json")


#Route for deleting asset from register
@app.route("/api/register/<int:id>", methods = ["DELETE"])
@decorators.accept("application/json")
def delete_asset(barcode):
    """ Delete a single asset from register """
    asset = session.query(models.Asset).get(barcode)
    
    if not asset:
        message = "Asset with barcode number {}".format(barcode)
        data = json.dumps({"message": message})
        return Response(data,404, mimetype = "application/json")
        
    #Delete the asset from database
    session.delete(asset)
    session.commit()
    assets = session.query(models.Asset).first()
    data=json.dumps(assets.as_dictionary(), indent=4, sort_keys=True, default=str)
    return Response(data, 200, mimetype = "application/json")
