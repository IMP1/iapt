import md5, time, os

def index():
	# If there is a user logged in, return their projects to the view
	response.title = 'Your Projects'
	auth_required('You must be logged in to see your projects.')
	return dict(projects=projects.users_projects(current_user, db))

def new():
	# Title the page
	response.title = 'New Project'
	# Create forms to create a project if a user is logged in
	auth_required('You must be logged in to create a project.')
	if len(request.args) > 0:
		step = int(request.args[0])
	else:
		# Clear existing session, the user probably doesn't want it if they've revisited...
		session.new_project = None
		step = 1
	# Do each step.
	if step == 1:
		# First step, project title.
		form = SQLFORM.factory(
			Field('title', 'string', requires=db.Project.title.requires),
			submit_button='Next >'
			)
		# Either create or prefill.
		if session.new_project == None:
			session.new_project = { 'documents' : [], 'sections' : [{'title':'', 'blurb':''}] }
		else:
			form.custom.widget.title['_value'] = session.new_project['title']

		if form.process().accepted:
			session.new_project['title'] = request.vars.title
			redirect(URL(args=[2]))
		# Return the step 1 form and the current step to the view
		return dict(form=form, step=step)
	elif step == 2:
		# Second step, document uploads.
		form = SQLFORM.factory(
			Field('title', 'string', requires=db.Document.title.requires),
			Field('image', 'upload', uploadfolder='documents', requires=db.Document.image.requires),
			submit_button='Add Document'
			)
		# User deleted a document?
		if (len(request.args) == 3) and (request.args[1] == 'delete'):
			# we could delete the image here, if we wanted.
			del session.new_project['documents'][int(request.args[2])]
			redirect(URL(args=[2]))
		# User added a new document?
		elif form.process(message_onsuccess={'msg': 'Document Added!', 'class': 'success_flash'}).accepted:
			# Save the image somewhere.
			hash =  md5.new(request.vars.image.filename + str(time.time()))
			iname = hash.hexdigest() + '.' + request.vars.image.filename.split('.')[-1]
			ipath = os.path.join(request.folder,'uploads', iname)
			ifile = open(ipath, 'wb')
			ifile.write(request.vars.image.value)
			ifile.close()
			session.new_project['documents'].append({
					'title' : request.vars.title,
					'image' : iname
				})
		# Return the current project, step 2 form and the current step to the view
		return dict(new_project=session.new_project, form=form, step=step)
	elif step == 3:
		if len(session.new_project['documents']) == 0:
			session.flash = {'msg': 'You must include at least one document.', 'class': 'error_flash'}
			redirect(URL(args=[2]))
		#Final step, project sections. N.B. must be at least 1 doc...
		if request.env.request_method == 'POST':
			# Update the session to be current field values.
			for i, s in enumerate(session.new_project['sections']):
				s['title'] = request.vars['section-title'+str(i)]
				s['blurb'] = request.vars['section-blurb'+str(i)]
			# Perform task based on url
			if request.args[1] == 'finish':
				# Check they have sections.
				if len(session.new_project['sections']) == 0:
					response.flash = "A project must have at least one section."
					return dict(new_project=session.new_project, step=step)
				# Check what they've entered.
				empty = False
				for s in session.new_project['sections']:
					empty |= (s['title'] == '') or (s['blurb'] == '')
				if empty:
					response.flash = "A title and description must be provided for all sections."
					return dict(new_project=session.new_project, step=step)
				# Create the project from the session.
				proj = projects.create(session.new_project['title'], current_user, db)
				# Create documents.
				docs = map(lambda d: documents.create(d['title'], proj, d['image'], db), session.new_project['documents'])
				# Create sections.
				secs = map(lambda s: sections.create(s['title'], s['blurb'], proj, db), session.new_project['sections'])
				# Clear the new project session
				session.new_project = None
				session.flash = {'msg': 'Project successfully created!', 'class': 'success_flash'}
				redirect(URL(f='manage', args=[proj.getId()]))
			elif request.args[1] == 'back':
				# Redirect the user back, now we've saved their data.
				redirect(URL(args=[2]))
			elif request.args[1] == 'remove':
				# Delete requested section.
				del session.new_project['sections'][int(request.args[2])]
				redirect(URL(args=[3]))
			elif request.args[1] == 'add':
				# Add a blank section.
				session.new_project['sections'].append({'title':'','blurb':''})
				redirect(URL(args=[3]))
		# Return the current project and the current step to the view
		return dict(new_project=session.new_project, step=step)
	else:
		# Return the step to the view
		return dict(step=step)

# TODO: Handle errors.
def manage():
	auth_required('You must be logged in to manage a project.')
	# Retrieve project.
	project = projects.Project(request.args[0], db)
	# Title the page
	response.title = 'Manage: ' + project.getTitle()
	# Check project owner.
	if current_user.getId() != project.getCreator():
		session.flash = 'You can not manage this project.'
		redirect(URL(c='project', f='index'))
	# Return the project to the view
	return dict(project=project)

def view():
	# Get project
	project = projects.Project(request.args[0], db)
	# Title the page
	response.title = 'Project: ' + project.getTitle()
	# Return the project to the view
	return dict(project=project)

def toggle():
	# Require login
	auth_required('You must be logged in to open or close a project.')
	# Get project
	project = projects.Project(request.args[0], db)
	# If user logged in is not creator, throw error
	if (project.getCreator() != current_user.getId()):
		session.flash = 'You can not open or close a project that you did not create.'
	# Change an open project to closed or vice versa
	else:
		project.setOpen(not project.isOpen())
		session.flash = {'msg': 'Project successfully ' + 
						('opened.' if project.isOpen() else 'closed.'),
						 'class': 'success_flash'}
	if request.env.http_referer:
		redirect(request.env.http_referer)
	else:
		redirect(URL(f='index'))

def image():
	# Stream the image without using db.
	filename=request.args[0]
	path=os.path.join(request.folder,'uploads',filename)
	response.headers['ContentType'] ="application/octet-stream";
	response.headers['Content-Disposition']="attachment; filename="+filename
	return response.stream(open(path, 'rb'),chunk_size=4096)
