# -*- coding: utf-8 -*-
# ORM for Projects.
import documents
import sections

def create(title, user, db):
	""" Create a new project.
		Returns the Project object for new project.

	Keyword arguments:
	title -- Title of the new project.
	user -- User object for creator.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Project.insert(creator=user.getId(), title=title, open=False)
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
		self._documents = None
		self._sections = None

	def getId(self):
		return self._data.id

	def getTitle(self):
		return self._data.title

	def setTitle(self, title):
		self._db(self._db.Project.id == self._data.id).update(title=title)
		self._data.title = title

	def getCreator(self):
		return self._data.creator
    
	def getDocumentCount(self):
		return self._db(self._db.Document.project == self._data.id).count()
    
	def getDocuments(self):
		# Lazy load documents.
		if self._documents == None:
			self._documents = list()
			docs = self._db(self._db.Document.project == self._data.id).select()
			for d in docs:
				self._documents.append(documents.Document(d.id, self._db))
		return self._documents
    
	def getSections(self):
		# Lazy load sections
		if self._sections == None:
			self._sections = list()
			for s in self._db(self._db.Section.project == self._data.id).select():
				self._sections.append(sections.Section(s.id, self._db))
		return self._sections

	def getDocumentsTranscribed(self):
		return len(self._db(
						(self._db.Document.id == self._db.Transcription.document) 
						& (self._db.Document.project == self._data.id)
						).select(groupby=self._db.Document.id))

	def isOpen(self):
		return self._data.open

	def setOpen(self, value):
		self._db(self._db.Project.id == self._data.id).update(open=value)
		self._data.open = value
