import os

def review():
	doc = documents.Document(request.args[0], db)
	response.title = 'Review: ' + doc.getTitle()
	print(request.vars)
	# Return the document to the view
	return dict(document=doc)

def transcribe():
	doc = documents.Document(request.args[0], db)
	response.title = 'Transcribe: ' + doc.getTitle()
	if request.env.request_method == 'POST':
		# Process sections.
		for section in doc.getProject().getSections():
			transcriptions.create(section, doc, request.vars['section'+str(section.getId())], db)
		# Redirect the user to wherever is appropriate.
		session.flash = {'msg': "Thank you for transcribing '" + doc.getTitle() + "'",
						 'class': 'success_flash'}
		redirect(URL(c='default', f='index'))
	return dict(document=doc)

def image():
	# Stream the image without using db.
	filename=request.args[0]
	path=os.path.join(request.folder,'uploads',filename)
	response.headers['ContentType'] ="application/octet-stream";
	response.headers['Content-Disposition']="attachment; filename="+filename
	return response.stream(open(path, 'rb'),chunk_size=4096)