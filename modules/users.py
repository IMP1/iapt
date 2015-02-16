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


def auth(session, db):
	""" Authenticate a user in database and return a user object.
		Returns user object or None if auth fails.

	Keyword arguments:
	session -- Instance of session.

	"""
	if (session.auth != None) and db(db.User.id == session.auth).count() == 1:
		return User(session.auth, db)
	else:
		return None 

class User(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.User.id == id).first()

	def getUsername(self):
		return self._data.username

	def setUsername(self, username):
		pass


	def setPassword(self, password):
		pass

		
