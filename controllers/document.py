def edit():
	return dict(document=documents.Document(request.args[0], db))

def transcribe():
	pass