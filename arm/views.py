from flask import Flask
from flask_login import login_user, logout_user

from . import app
from . database import session, User

# solves most responses you need
from flask import render_template, request, redirect, url_for, flash

# if authentication is needed, this is where you start
from flask_login import login_required, login_user, current_user
from werkzeug.security import check_password_hash

@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')


PAGINATE_BY = 20

# Landing page that gives you access to the full asset register
@app.route("/")
@app.route("/page/<int:page>")
def assets_register(page = 1):
	# Index for page Zero
	page_index = page - 1

	#Get the total number of assets in the register
	assets_count = session.query(Asset).count()

	#Indicate start and end of pages
	start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    #Navigation between pages
    total_pages = (count - 1) // PAGINATE_BY + 1
    next_page = page_index < total_pages - 1
    prev_page = page_index > 0

    #Query register for assets to display
    assets = session.query(Asset)
    assets = assets.order_by(Asset.barcode.asc())
    assets = assets[start:end]

    #Render assets from query results to html
    return render_template("assets_register.html",
        assets = assets,
        next_page = next_page,
        prev_page = prev_page,
        page = page,
        total_pages = total_pages
    )