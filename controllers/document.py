def review():
	return dict(document=documents.Document(request.args[0], db))

def new():
	#doc = documents.create('New Document', projects.Project(request.args[0], db), '', db)
	project = projects.Project(request.args[0], db)

	form = SQLFORM(db.Document, fields=['title', 'image'])
	# Fill out excluded information
	form.vars.project = project.getId()
	form.vars.status = 1
	# Customise form
	form.custom.widget.title['_placeholder'] = 'Document Title'
	if form.process().accepted:
		redirect(URL(c='project', f='edit', args=[project.getId()]))
	return dict(form=form, project=project)

def transcribe():
	document = documents.Document(request.args[0], db)
	return dict(document=document)

def image():
	return response.download(request, db)