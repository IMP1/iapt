# -*- coding: utf-8 -*-
# ORM for Transcriptions.

def create(section, text, db):
	""" Create a new section.
		Returns the Section object for new section.

	Keyword arguments:
	section -- Object for corresponding section.
	text -- Transcription text.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Transcription.insert(section=section.getId(), text=text, accepted=False)
	return Transcription(id, db)

class Transcription(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Transcription.id == id).select().first()
