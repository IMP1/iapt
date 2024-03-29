import os
import transcriptions

def review():
	# Require user to be logged in
	auth_required('You must be logged in to review a document.')
	# Get document
	doc = documents.Document(request.args[0], db)
	# Title the page
	response.title = 'Review: ' + doc.getTitle()
	# Redirect to view page if transcriptions have been accepted
	if doc.isAccepted():
		redirect(URL(c='document', f='view', args=[doc.getId()]))
	# If user selects to accept transcriptions, accept them
	if request.vars.action == "accept":
		for section in doc.getProject().getSections():
			# Accept chosen transcriptions
			if ("section" + str(section.getId())) in request.vars:
				tid = int(request.vars["section" + str(section.getId())])
				transcriptions.accept(tid, db)
			# Delete the others
			for transcription in doc.getTranscriptions(section):
				if not transcription.isAccepted():
					transcriptions.delete(transcription.getId(), db)
		# Redirect to view
		session.flash = {'msg': "You've accepted the following transcriptions and the document has been closed.",
						 'class': 'success_flash'}
		redirect(URL(c='document', f='view', args=[doc.getId()]))
	# If user selects to reject transcriptions, reject them
	elif request.vars.action == "reject":
		# Delete all the transcriptions
		for section in doc.getProject().getSections():
			for transcription in doc.getTranscriptions(section):
				transcriptions.delete(transcription.getId(), db)
		# Redirect to the project page.
		session.flash = {'msg': "The document has been reopened, rejecting all transcriptions.",
						 'class': 'success_flash'}
		redirect(URL(c='project', f='index'))
	# Return the document to the view
	return dict(document=doc)

def view():
	# Get document
	doc = documents.Document(request.args[0], db)
	# Title the page
	response.title = 'View: ' + doc.getTitle()
	# If transcriptions have not been reviewed and accepted, redirect to review page
	if not doc.isAccepted():
		redirect(URL(c='document', f='review', args=[doc.getId()]))
	# Return the document to the view
	return dict(document=doc)

def transcribe():
	# Get document
	doc = documents.Document(request.args[0], db)
	# Title the page
	response.title = 'Transcribe: ' + doc.getTitle()
	if request.env.request_method == 'POST':
		# Check there is at least one transcription.
		count = 0
		for section in doc.getProject().getSections():
			if request.vars['section'+str(section.getId())].strip():
				count += 1
		if count == 0:
			response.flash = "You must transcribe at least one section."
		else:
			# Process sections.
			for section in doc.getProject().getSections():
				transcriptions.create(section, doc, request.vars['section'+str(section.getId())], db)
			# Redirect the user to wherever is appropriate.
			session.flash = {'msg': "Thank you for transcribing '" + doc.getTitle() + "'. You might be interested in other documents in this project.",
							 'class': 'success_flash'}
			redirect(URL(c='project', f='view', args=doc.getProject().getId()))
	# Return the document and project to the view
	return dict(document=doc, project=doc.getProject())

def image():
	# Stream the image without using db.
	filename=request.args[0]
	path=os.path.join(request.folder,'uploads',filename)
	response.headers['ContentType'] ="application/octet-stream";
	response.headers['Content-Disposition']="attachment; filename="+filename
	return response.stream(open(path, 'rb'),chunk_size=4096)

def browse():
	# Title page
	response.title = 'All Documents'
	# Return all documents to the view
	return dict(docs=documents.search_results(db, ""))