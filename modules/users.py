# -*- coding: utf-8 -*-
# ORM for Users.

def register(uname, password, db):
	""" Register a user in database and return a user object.

	Keyword arguments:
	uname -- The username for the new user.
	password -- The password for the new user.
	db -- Instance of db (DAL) in use.

	"""
	db.User.insert(**db.User._filter_fields(dict(username=uname, password=password)))

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

def unauth(session):
	""" Un-authenticate a user.

	Keyword arguments:
	session -- Instance of session.
	"""
	session.auth = None

class User(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.User.id == id).select().first()

	def getUsername(self):
		return self._data.username

	def setUsername(self, uname):
		db(db.User.id == self._data.id).update(username=uname)

	def setPassword(self, pword):
		db(db.User.id == self._data.id).update(password=pword)

		
