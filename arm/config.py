import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://zak:thinkful@localhost:5432/armapp"
	DEBUG = True
	SECRET_KEY = os.environ.get("FARMAPP_SECRET_KEY", os.urandom(12))

	# Flask-Mail SMTP server settings
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	MAIL_USERNAME = 'empty@arcplusapp.com'
	MAIL_PASSWORD = 'empty'
	MAIL_DEFAULT_SENDER = '"ARCPlus" <noreply@arcplusapp.com>'

    # Flask-User settings
	USER_APP_NAME = "ARCPlus Software"      	# Shown in and email templates and page footers
	USER_ENABLE_EMAIL = True        			# Enable email authentication
	USER_ENABLE_USERNAME = True    				# Enable username authentication
	USER_EMAIL_SENDER_NAME = USER_APP_NAME
	USER_EMAIL_SENDER_EMAIL = "noreply@arcpluapp.com"


class TestingConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://zak:thinkful@localhost:5432/armappstest"
	DEBUG = True
	SECRET_KEY = os.environ.get("FARMAPP_SECRET_KEY", os.urandom(12))
