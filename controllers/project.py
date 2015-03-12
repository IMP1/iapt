import md5, time, os

def index():
	# If there is a user logged in, return their projects to the view
	auth_required('You must be logged in to see your projects.')
	return dict(projects=projects.users_projects(current_user, db))

def new():
	# Create forms to create a project if a user is logged in
	auth_required('You must be logged in to create a project.')
	step = int(request.args[0]) if len(request.args) == 1 else 1
	if step == 1:
		# First step, project title.
		form = SQLFORM.factory(
			Field('title', 'string', requires=IS_NOT_EMPTY()),
			submit_button='Next >'
			)
		if form.process().accepted:
			session.new_project = {	'title' : request.vars.title,
									'documents' : [] }
			redirect(URL(args=[2]))
		# Return the step 1 form and the current step to the view
		return dict(form=form, step=step)
	elif step == 2:
		# Second step, document uploads.
		form = SQLFORM.factory(
			Field('title', 'string', requires=IS_NOT_EMPTY()),
			Field('image', 'upload', uploadfolder='documents', requires=IS_NOT_EMPTY()),
			submit_button='Upload'
			)
		if form.process().accepted:
			# Save the image somewhere.
			hash =  md5.new(request.vars.image.filename + str(time.time()))
			iname = hash.hexdigest() + '.' + request.vars.image.filename.split('.')[-1]
			ipath = os.path.join(request.folder,'uploads', iname)
			ifile = open(ipath, 'w')
			ifile.write(request.vars.image.value)
			session.new_project['documents'].append({
					'title' : request.vars.title,
					'image' : iname
				})
		# Return the current project, step 2 form and the current step to the view
		return dict(new_project=session.new_project, form=form, step=step)
	elif step == 3:
		#Final step, project sections. N.b. must be at least 1 doc...
		# Return the current project and the current step to the view
		return dict(new_project=session.new_project, step=step)
	else:
		# Return the step to the view
		return dict(step=step)

# TODO: Handle errors.
def manage():
	auth_required('You must be logged in to edit a project.')
	# Retrieve project.
	project = projects.Project(request.args[0], db)
	# Check project owner.
	if current_user.getId() != project.getCreator():
		session.flash = 'You can not edit this project.'
		redirect(URL(c='project', f='index'))
	# Return the project to the view
	return dict(project=project)

def view():
	# Return the project to the view
	return dict(project=projects.Project(request.args[0], db))

def image():
	# Stream the image without using db.
	filename=request.args[0]
	path=os.path.join(request.folder,'uploads',filename)
	response.headers['ContentType'] ="application/octet-stream";
	response.headers['Content-Disposition']="attachment; filename="+filename
	return response.stream(open(path),chunk_size=4096)
