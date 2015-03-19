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

	def getTranscriptions(self):
		# Lazy load transcriptions
		if self._transcriptions == None:
			self._transcriptions = list()
			trans = self._db(self._db.Transcription.section == self._data.id).select()
			for t in trans:
				self._transcriptions.append(transcriptions.Transcription(t.id, self._db))
		return self._transcriptions

	def getId(self):
		return self._data.id

	def getTitle(self):
		return self._data.title

	def getBlurb(self):
		return self._data.blurb
