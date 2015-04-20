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
							 image=image)
	return Document(id, db)

def recent_documents(db):
	""" Get the 10 most recent documents
		Returns list of 10 recent documents

	Keyword arguments:
	db -- Instance of db (DAL) in use.

	"""	
	ret_list = list()
	results = db(db.Document).select(orderby=~db.Document.id)
	limit = 10
	for r in results:
		doc = Document(r.id, db)
		if limit > 0 and doc.isOpen():
			ret_list.append(doc)
			limit -= 1
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
	document_results = db(db.Document.title.like(term) | ((db.Project.title.like(term)) & (db.Document.project == db.Project.id))).select(db.Document.ALL, distinct=True)
	for r in document_results:
		doc = Document(r.id, db)
		if doc.isOpen():
			ret_list.append(doc)
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
		# Returns the document's title
		return self._data.title

	def getId(self):
		# Returns the document's ID
		return self._data.id

	def getImage(self):
		# Returns the document's image
		return self._data.image

	def getProject(self):
		# Lazy load project.
		if self._project == None:
			self._project = projects.Project(self._data.project, self._db)
		# Returns the project that the document is part of
		return self._project

	def isAccepted(self):
		# Returns whether or not the document's transcriptions have been accepted
		return self._db((self._db.Transcription.document == self._data.id) & (self._db.Transcription.accepted == True)).count() > 0

	def getTranscriptionCount(self):
		section_count = len(self.getProject().getSections())
		# Returns the number of transcriptions made to the document
		return self._db(self._db.Transcription.document == self._data.id).count() // section_count

	def getTranscriptions(self, section):
		# Lazy load transcriptions
		if self._transcriptions == None:
			self._transcriptions = dict()
		if not section in self._transcriptions:
			self._transcriptions[section] = list()
			trans = self._db((self._db.Transcription.document == self._data.id) & (self._db.Transcription.section == section.getId())).select()
			for t in trans:
				self._transcriptions[section].append(transcriptions.Transcription(t.id, self._db))
		# Returns the transcriptions made to the document
		return self._transcriptions[section]

	def getAcceptedTranscription(self, section):
		# Returns the transcription that has been accepted
		return self._db((self._db.Transcription.document == self._data.id) 
						& (self._db.Transcription.section == section.getId()) 
						& (self._db.Transcription.accepted == True)).select().first()
    
	def isOpen(self):
		# Returns whether ot not the document is open for transcriptions
		return self.getTranscriptionCount() < 3 and not self.isAccepted() and self.getProject().isOpen()
        