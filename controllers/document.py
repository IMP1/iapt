import os

def review():
	# Return the document to the view
	return dict(document=documents.Document(request.args[0], db))

def transcribe():
	document = documents.Document(request.args[0], db)
	sections = document.getProject().getSections()
	print(sections)
	return dict(document=document, sections=sections)

def image():
	# Stream the image without using db.
	filename=request.args[0]
	path=os.path.join(request.folder,'uploads',filename)
	response.headers['ContentType'] ="application/octet-stream";
	response.headers['Content-Disposition']="attachment; filename="+filename
	print path
	return response.stream(open(path, 'rb'),chunk_size=4096)