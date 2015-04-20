# -*- coding: utf-8 -*-
# ORM for Sections.
import transcriptions

def create(title, blurb, project, db):
	""" Create a new section.
		Returns the Section object for new section.

	Keyword arguments:
	title -- Title of the new section.
	blurb -- Short description of section.
	project -- The project object that this section belongs to.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Section.insert(title=title, blurb=blurb, project=project.getId())
	return Section(id, db)

class Section(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Section.id == id).select().first()
		self._transcriptions = None

	def getTranscriptions(self, document):
		# Lazy load transcriptions
		if self._transcriptions == None:
			self._transcriptions = dict()
		if not document in self._transcriptions:
			self._transcriptions[document] = list()
			trans = self._db((self._db.Transcription.section == self._data.id) & (self._db.Transcription.document == document.getId())).select()
			for t in trans:
				self._transcriptions[document].append(transcriptions.Transcription(t.id, self._db))
		# Returns the transcriptions made to a particular section in a particular document
		return self._transcriptions[document]

	def getId(self):
		# Returns the section's ID
		return self._data.id

	def getTitle(self):
		# Returns the section's title
		return self._data.title

	def getBlurb(self):
		# Returns the section's blurb/description
		return self._data.blurb
		