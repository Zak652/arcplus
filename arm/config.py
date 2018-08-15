import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://zak:thinkful@localhost:5432/armapp"
	DEBUG = True
	SECRET_KEY = os.environ.get("FARMAPP_SECRET_KEY", os.urandom(12))


class TestingConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://zak:thinkful@localhost:5432/armapptest"
	DEBUG = True
	SECRET_KEY = os.environ.get("FARMAPP_SECRET_KEY", os.urandom(12))
