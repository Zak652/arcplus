import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql:///arcplus"
	DEBUG = True
	SECRET_KEY = os.environ.get("ARCPLUS_SECRET_KEY", os.urandom(12))

	# Flask security
	# SECURITY_URL_PREFIX = "/register/view"
	SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
	SECURITY_PASSWORD_SALT = "ATGUOHAELKampalaughaerGOJAEGj"


	SECURITY_UNAUTHORIZED_VIEW = '/user/login'
	SECURITY_LOGIN_URL = "/user/login"
	SECURITY_LOGOUT_URL = "/user/logout"

	SECURITY_POST_LOGIN_VIEW = "/register/view"
	SECURITY_POST_LOGOUT_VIEW = "/user/login"
	SECURITY_CHANGE_URL = "/user/change_password"

	SECURITY_POST_CHANGE_VIEW = "/user/logout"

	# Flask-Security features
	SECURITY_REGISTERABLE = False
	SECURITY_CHANGEABLE = True
	SECURITY_SEND_REGISTER_EMAIL = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	SECURITY_TRACKABLE = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True

	# Flask-Mail SMTP server settings
	# MAIL_SERVER = 'smtp.gmail.com'
	# MAIL_PORT = 465
	# MAIL_USE_SSL = True
	# MAIL_USE_TLS = False
	# MAIL_USERNAME = 'username'
	# MAIL_PASSWORD = 'password'


class TestingConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql:///arcplustest"
	DEBUG = True
	SECRET_KEY = os.environ.get("ARCPLUS_SECRET_KEY", os.urandom(12))
