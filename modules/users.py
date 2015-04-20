# -*- coding: utf-8 -*-
# ORM for Users.
from gluon.validators import Validator

def register(uname, password, db):
	""" Register a user in database and return a user object.

	Keyword arguments:
	uname -- The username for the new user.
	password -- The password for the new user.
	db -- Instance of db (DAL) in use.
	"""
	id = db.User.insert(username=uname, password=password)
	return User(id, db)

def login(uname, password, db, session):
	""" Login a user in database and return true on success.

	Keyword arguments:
	uname -- The username for the new user.
	password -- The password for the new user.
	db -- Instance of db (DAL) in use.
	session -- Instance of session.
	"""
	query = db((db.User.username == uname) & (db.User.password == password))
	if query.count() == 1:
		session.auth = query.select().first().id
		return True
	else:
		return False

def correct_password(username, password, db):
	""" Checks whether the username/password combination exists in the database.

	Keyword arguments:
	usernamename -- The username for the user.
	password -- The password for the user.
	db -- Instance of db (DAL) in use.
	"""
	query = db((db.User.username == username) & (db.User.password == password))
	return query.count() > 0

def auth(session, db):
	""" Authenticate a user in database and return a user object.
		Returns user object or None if auth fails.

	Keyword arguments:
	session -- Instance of session.
	db -- Instance of db (DAL) in use.
	"""
	if (session.auth != None) and db(db.User.id == session.auth).count() == 1:
		return User(session.auth, db)
	else:
		return None 

def deauth(session):
	""" deauthenticate a user.

	Keyword arguments:
	session -- Instance of session.
	"""
	session.auth = None

class IS_NOT_IN_USE(Validator):
	# Error class used to return useful error messages.
	def __init__(self, other, error_message='Username already in use'):
		self.db = other
		self.error_message = error_message

	def __call__(self, value):
		error = None
		if self.db(self.db.User.username == value).count() != 0:
			error = self.error_message
		return (value, error)

class User(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.User.id == id).select().first()

	def getId(self):
		# Returns the user's ID
		return self._data.id

	def getUsername(self):
		# Returns the user's username
		return self._data.username

	def setUsername(self, uname):
		# Changes the user's username
		self._db(self._db.User.id == self._data.id).update(username=uname)
		self._data.username = uname

	def setPassword(self, pword):
		# Changes the user's password
		self._db(self._db.User.id == self._data.id).update(password=pword)
		self._data.password = pword

