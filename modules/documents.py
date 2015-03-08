# -*- coding: utf-8 -*-
# ORM for Documents.
import projects

class Document(object):
	def __init__(self, id, db, get_project=True):
		""" Constructor for documents.

		Keyword arguments:
		id -- id of document for object.
		db -- Instance of db (DAL) in use.
		get_project -- whether or not to get project, to stop recursion.

		"""
		self._db = db
		self._data = db(db.Document.id == id).select().first()
		if get_project:
			self._project = projects.Project(self._data.project, self._db)
		else:
			self._project = None

	def getTitle(self):
		return self._data.title

	def getId(self):
		return self._data.id

	def getProject(self):
		return self._project

