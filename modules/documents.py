# -*- coding: utf-8 -*-
# ORM for Documents.
import projects

def search_results(db, searchterm):
	""" Get the documents with titles like searchterm
		Returns a list of projects

	Keyword arguments:
	db -- Instance of db (DAL) in use.
	searchterm -- text entered in searchbar

	"""
	ret_list = list()
	term = "%"+searchterm+"%"
	results = db((db.Document.title.like(term))).select()
	for r in results:
		ret_list.append(Document(r.id, db))
	return ret_list

class Document(object):
	def __init__(self, id, db):
		""" Constructor for documents.

		Keyword arguments:
		id -- id of document for object.
		db -- Instance of db (DAL) in use.
		get_project -- whether or not to get project, to stop recursion.

		"""
		self._db = db
		self._data = db(db.Document.id == id).select().first()
		self._project = None

	def getTitle(self):
		return self._data.title

	def getId(self):
		return self._data.id

	def getImage(self):
		return self._data.image

	def getProject(self):
		# Lazy load project.
		if self._project == None:
			self._project = projects.Project(self._data.project, self._db)
		return self._project

