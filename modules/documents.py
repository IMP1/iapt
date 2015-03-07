# ORM for Documents.
def create(title, project, image, db):
	""" Create a new document and return document object.

	Keyword arguments:
	title -- The title for the new document.
	project -- The parent project for the new  document.
	image -- The image for the new document.
	db -- Instance of db (DAL) in use.

	"""
	id = db.Documnent.insert(title=title, project=project.getId(),
							 image=image, status=doc_statuses.index('Closed'))
	return Document(id, db)

class Document(object):
	def __init__(self, id, db):
		self._db = db
		self._data = db(db.Document.id == id).select().first()

	def getTitle(self):
		return self._data.title

	def getId(self):
		return self._data.id

