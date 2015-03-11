import base64

def index():
	auth_required('You must be logged in to see your projects.')
	return dict(projects=projects.users_projects(current_user, db))

def new():
	auth_required('You must be logged in to create a project.')
	step = int(request.args[0]) if len(request.args) == 1 else 1
	if step == 1:
		#First step, project title.
		form = SQLFORM.factory(
			Field('title', 'string', requires=IS_NOT_EMPTY()),
			submit_button='Next >'
			)
		if form.process().accepted:
			session.new_project = {	'title' : request.vars.title,
									'documents' : [] }
		return dict(form=form, step=step)
	elif step == 2:
		#Second step, document uploads.
		form = SQLFORM.factory(
			Field('title', 'string', requires=IS_NOT_EMPTY()),
			Field('image', 'upload', uploadfolder='documents'),
			submit_button='Upload'
			)
		if form.process().accepted:
			session.new_project['documents'].append({
					'title' : request.vars.title,
					'image' : base64.b64encode(request.vars.image.value)
				})
		return dict(new_project=session.new_project, form=form, step=step)
	elif step == 3:
		#Final step, project sections.
		return dict(step=step)
	else:
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
	return dict(project=project)

def view():
	project = projects.Project(request.args[0], db)
	return dict(project=project)