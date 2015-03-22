# -*- coding: utf-8 -*-
# ORM for Documents.
import projects
import transcriptions

def create(title, project, image, db):
	""" Create a new document and return document object.
	Keyword arguments:
	title -- The title for the new document.
	project -- The parent project object for the new document.
	image -- The image for the new document.
	db -- Instance of db (DAL) in use.
	"""
	id = db.Document.insert(title=title, project=project.getId(),
							 image=image, status=1)
	return Document(id, db)

def recent_documents(db):
	""" Get the 9 most recent documents
		Returns list of 9 recent documents

	Keyword arguments:
	db -- Instance of db (DAL) in use.

	"""	
	ret_list = list()
	results = db(db.Document).select(orderby=~db.Document.id,limitby=(0,9))
	for r in results:
		ret_list.append(Document(r.id, db))
	return ret_list

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
		self._transcriptions = None

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

	def isAccepted(self):
		return self._db((self._db.Transcription.document == self._data.id) & (self._db.Transcription.accepted == True)).count() > 0

	def getTranscriptionCount(self):
		return self._db(self._db.Transcription.document == self._data.id).count()

	def getTranscriptions(self, section):
		# Lazy load transcriptions
		if self._transcriptions == None:
			self._transcriptions = dict()
		if not section in self._transcriptions:
			self._transcriptions[section] = list()
			trans = self._db((self._db.Transcription.document == self._data.id) & (self._db.Transcription.section == section.getId())).select()
			for t in trans:
				self._transcriptions[section].append(transcriptions.Transcription(t.id, self._db))
		return self._transcriptions[section]

	def getAcceptedTranscription(self, section):
		return self._db((self._db.Transcription.document == self._data.id) & (self._db.Transcription.section == section.getId()) & (self._db.Transcription.accepted == True)).select().first()