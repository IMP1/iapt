def index():
	if user != None:
		users.unauth(session)
	redirect(URL(c='default'))