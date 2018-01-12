#This file is for configuring all application related forms

from wtforms import Form, StringField, IntegerField, SelectField

asset_categories = [('Buildings', 'Buildings'), ('Furniture', 'Furniture'), ('Computers', 'Computers')]
asset_types = [('Commercial', 'Commercial'), ('Chair', 'Chair'), ('Laptop', 'Laptop')]
asset_models = [('Mall', 'Mall'), ('Office Chair', 'Office Chair'), ('Thinkpad X1', 'Thinkpad X1')]
status_modes = [('Active', 'Active'), ('Inactive', 'Inactive')]
asset_locations = [('Kampala', 'Kampala'), ('Nairobi', 'Nairobi'), ('London', 'London')]
users = [('Tom', 'Tom'), ('Dan', 'Dan'), ('Moses', 'Moses')]
suppliers = [('Roko', 'Roko'), ('Footsteps', 'Footsteps'), ('Lenovo', 'Lenovo')]

class AddAssetForm(Form):
	barcode = StringField('Barcode')
	serial_no = StringField('Serial No.')
	name = StringField('Asset Name')
	category = SelectField('Asset Category', choices = asset_categories)
	_type = SelectField('Asset Type', choices = asset_types)
	_model = SelectField('Asset Model', choices = asset_models)
	status = SelectField('Status', choices = status_modes)
	location = SelectField('Asset Location', choices = asset_locations)
	user = SelectField('Asset User', choices = users)
	purchase_price = IntegerField('Purchase Price')
	supplier = SelectField('Supplier' choices = suppliers)
