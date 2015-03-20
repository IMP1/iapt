# -*- coding: utf-8 -*-
# ORM for Transcriptions.

def create(section, document, text, db):
	""" Create a new transcription.
		Returns the transcription object for new transcription.

	Keyword arguments:
	section -- Object for corresponding section.
    document -- Object for corresponding document.
	text -- Transcription text.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Transcription.insert(section=section.getId(), document=document.getId(), text=text, accepted=False)
	return Transcription(id, db)

class Transcription(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Transcription.id == id).select().first()

	def getId(self):
		return self._data.id
