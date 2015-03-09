def index():
	auth_required('You must be logged in to see your projects.')
	return dict(projects=projects.users_projects(current_user, db))

def new():
	auth_required('You must be logged in to create a project.')
	flow = int(request.args[0]) if len(request.args) == 1 else 0
	form = SQLFORM.factory(
			Field('title', 'string', requires=IS_NOT_EMPTY()),
			submit_button='Create Project'
			)
	if form.process().accepted:
		redirect(URL(c='project', f='edit', args=[projects.create(form.vars.title, current_user, db).getId()]))
	return dict(form=form)

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
