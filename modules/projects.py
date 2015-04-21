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

class Project(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Project.id == id).select().first()
		self._documents = None
		self._sections = None

	def getId(self):
		# Returns the project's ID
		return self._data.id

	def getTitle(self):
		# Returns the project's title
		return self._data.title

	def setTitle(self, title):
		# Updates the project's title
		self._db(self._db.Project.id == self._data.id).update(title=title)
		self._data.title = title

	def getCreator(self):
		# Returns the user who created the project
		return self._data.creator

	def getDocumentCount(self):
		# Returns the number of documents in the project
		return self._db(self._db.Document.project == self._data.id).count()

	def getOpenDocumentCount(self):
		count = 0
		for doc in self.getDocuments():
			if doc.isOpen():
				count += 1
		# Returns the number of open documents in the project
		return count

	def getDocuments(self):
		# Lazy load documents.
		if self._documents == None:
			self._documents = list()
			docs = self._db(self._db.Document.project == self._data.id).select()
			for d in docs:
				self._documents.append(documents.Document(d.id, self._db))
		# Returns the project's documents
		return self._documents

	def getSections(self):
		# Lazy load sections
		if self._sections == None:
			self._sections = list()
			for s in self._db(self._db.Section.project == self._data.id).select():
				self._sections.append(sections.Section(s.id, self._db))
		# Returns the project's sections
		return self._sections

	def getDocumentsTranscribed(self):
		# Returns the number of documents transcribed
		return len(self._db(
						(self._db.Document.id == self._db.Transcription.document) 
						& (self._db.Document.project == self._data.id)
						).select(groupby=self._db.Document.id))

	def isOpen(self):
		# Returns whether or not the project is open
		return self._data.open

	def setOpen(self, value):
		# Updates whether or not the project is open
		self._db(self._db.Project.id == self._data.id).update(open=value)
		self._data.open = value
