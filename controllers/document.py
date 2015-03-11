def review():
	return dict(document=documents.Document(request.args[0], db))

def transcribe():
	document = documents.Document(request.args[0], db)
	return dict(document=document)

def image():
	return response.download(request, db)