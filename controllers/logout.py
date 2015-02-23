def index():
	if user != None:
		users.deauth(session)
	redirect(URL(c='default'))