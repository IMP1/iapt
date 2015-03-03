def index():
	if current_user != None:
		users.deauth(session)
	redirect(URL(c='default'))
