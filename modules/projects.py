# -*- coding: utf-8 -*-
# ORM for Projects.

def create(title, user, db):
	id = db.Project.insert(creator=user.getId(), title=title, status=2)
	return Project(id, db)

class Project(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Project.id == id).select().first()

	def getTitle(self):
		return self._data.title
