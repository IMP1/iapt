# ORM for Documents.
def create(title, image, db):
	""" Create a new document and return document object.

	Keyword arguments:
	title -- The title for the new document.
	image -- The image for the new document.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Documnent.insert(title=title, image=image, status=doc_statuses.index('Closed'))
	return Document(id, db)

class Document(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Document.id == id).select().first()
