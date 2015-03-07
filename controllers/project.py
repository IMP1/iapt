def index():
	if current_user == None:
		session.flash = 'You must be logged in to see your projects.'
		redirect(URL(c='user', f='login'))
	projects = [
				{'title':"Test Project 1"},
				{'title':"Test Project 2"}
				]
	return dict(projects=projects)

def new():
	if current_user == None:
		session.flash = 'You must be logged in to create a project.'
		redirect(URL(c='user', f='login'))
	return dict()
