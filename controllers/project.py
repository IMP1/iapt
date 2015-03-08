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
		projects.create(form.vars.title, current_user, db)
		# TODO: Redirect to manage this project.
		redirect(URL(c='project', f='index'))
	return dict(form=form)
