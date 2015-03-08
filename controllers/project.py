def index():
	if current_user == None:
		session.back = URL(args=request.args, host=True)
		session.flash = 'You must be logged in to see your projects.'
		redirect(URL(c='user', f='login'))
	return dict(projects=projects.users_projects(current_user, db))

def new():
	if current_user == None:
		session.back = URL(args=request.args, host=True)
		session.flash = 'You must be logged in to create a project.'
		redirect(URL(c='user', f='login'))
	form = SQLFORM.factory(
			Field('title', 'string', requires=IS_NOT_EMPTY()),
			submit_button='Create Project'
			)
	if form.process().accepted:
		
		# TODO: Redirect to manage this project.
		redirect(URL(c='project', f='edit', args=[projects.create(form.vars.title, current_user, db).getId()]))
	return dict(form=form)

# TODO: Handle errors.
def edit():
	# Must be logged in.
	if current_user == None:
		session.back = URL(args=request.args, host=True)
		session.flash = 'You must be logged in to edit a project.'
		redirect(URL(c='user', f='login'))
	# Retrieve project.
	project = projects.Project(request.args[0], db)
	# Check project owner.
	if current_user.getId() != project.getCreator():
		session.flash = 'You can not edit this project.'
		redirect(URL(c='project', f='index'))
	return dict(project=project)
