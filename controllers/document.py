def review():
	return dict(document=documents.Document(request.args[0], db))

def new():
	#doc = documents.create('New Document', projects.Project(request.args[0], db), '', db)
	return dict(project=projects.Project(request.args[0], db))

def transcribe():
	pass