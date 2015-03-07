def index():
	projects = [
				{'title':"Test Project 1"},
				{'title':"Test Project 2"}
				]
	return dict(projects=projects)

def new():
	return dict()