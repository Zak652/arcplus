from flask_table import Table, Col
 
class AssetsReg(Table):
    id = Col('ID', show = False)
	barcode = Col('Barcode', show = True)
	serial_no = Col('Serial No.', show = False)
	datetime = Col('Modified Date', show = True)
	name = Col('Name', show = True)
	category = Col('Category', show = True)
	_type = Col('Type', show = True)
	_model = Col('Model', show = True)
	status = Col('Status', show = True)
	location = Col('Location', show = True)
	user = Col('User', show = True)
	purchase_price = Col('Purchase Price', show = True)
	value = Col('Current Value', show = True)
	supplier = Col('Supplier', show = False)
	photo = Col('Photo', show = False)
	comments = Col('Comments', show = False)
	edit = LinkCol('Edit', 'edit', url_kwargs=dict(id = 'id'))
	