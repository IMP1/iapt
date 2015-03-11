def review():
	return dict(document=documents.Document(request.args[0], db))

def transcribe():
	return dict(document=documents.Document(request.args[0], db))

def image():
	return response.download(request, db)