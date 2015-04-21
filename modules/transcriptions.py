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

def accept(transcription_id, db):
	""" Accept a transcription.

	Keyword arguments:
	transcription_id -- Transcription to accept.
	db -- Instance of db (DAL) in use.

	"""
	db(db.Transcription.id == transcription_id).update(accepted=True)
    
def delete(transcription_id, db):
	""" Remove a transcription.

	Keyword arguments:
	transcription_id -- Transcription to accept.
	db -- Instance of db (DAL) in use.

	"""
	db(db.Transcription.id == transcription_id).delete()

class Transcription(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Transcription.id == id).select().first()

	def getId(self):
		# Returns the transcription's ID
		return self._data.id

	def getText(self):
		# Returns the transcription's tex
		return self._data.text

	def isAccepted(self):
		# Returns whether or not the transcription has been accepted
		return self._data.accepted
