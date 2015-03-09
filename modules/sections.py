# -*- coding: utf-8 -*-
# ORM for Sections.

class Section(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Section.id == id).select().first()
