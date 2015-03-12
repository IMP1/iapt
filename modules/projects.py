# -*- coding: utf-8 -*-
# ORM for Projects.
import documents

def create(title, user, db):
	""" Create a new project.
		Returns the Project object for new project.

	Keyword arguments:
	title -- Title of the new project.
	user -- User object for creator.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Project.insert(creator=user.getId(), title=title)
	return Project(id, db)

def users_projects(user, db):
	""" Get all projects belonging to user.
		Returns list of Project objects.

	Keyword arguments:
	user -- User object for creator.
	db -- Instance of db (DAL) in use.

	"""
	ret_list = list()
	results = db(db.Project.creator ==  user.getId()).select()
	for r in results:
		ret_list.append(Project(r.id, db))
	return ret_list

def recent_projects(db):
	""" Get the 9 most recent projects
		Returns list of 9 recent projects

	Keyword arguments:
	db -- Instance of db (DAL) in use.

	"""	
	ret_list = list()
	results = db(db.Project).select(orderby=~db.Project.id,limitby=(0,9))
	for r in results:
		ret_list.append(Project(r.id, db))
	return ret_list

def search_results(db, searchterm):
	""" Get the projects with titles like searchterm
		Returns a list of projects

	Keyword arguments:
	db -- Instance of db (DAL) in use.
	searchterm -- text entered in searchbar

	"""
	ret_list = list()
	term = "%"+searchterm+"%"
	results = db((db.Project.title.like(term))).select()
	for r in results:
		ret_list.append(Project(r.id, db))
	return ret_list

class Project(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Project.id == id).select().first()
		self._documents = list()
		docs = db(db.Document.project == id).select()
		for d in docs:
			self._documents.append(documents.Document(d.id, db, False))

	def getId(self):
		return self._data.id

	def getTitle(self):
		return self._data.title

	def setTitle(self, title):
		self._db(self._db.Project.id == self._data.id).update(title=title)
		self._data.title = title

	def getCreator(self):
		return self._data.creator

	def getDocuments(self):
		return self._documents
