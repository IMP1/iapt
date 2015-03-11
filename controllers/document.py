def review():
	# Return the document to the view
	return dict(document=documents.Document(request.args[0], db))

def transcribe():
	# Return the document to the view
	return dict(document=documents.Document(request.args[0], db))

def image():
	return response.download(request, db)