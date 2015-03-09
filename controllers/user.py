def index():
	auth_required('You must be logged in to see your profile.')
	unform = SQLFORM.factory(
		Field('username', length=128, label="New Username", default='')
		)
	if unform.process().accepted:
		current_user.setUsername(unform.vars.username)
	pwform = SQLFORM.factory(
		Field('password', 'password', length=64, label="New Password"),
		Field('cpassword', 'password', 
			label="Confirm Password",
			requires=IS_EQUAL_TO(request.vars.password, error_message='Passwords do not match.'))
		)
	if pwform.process().accepted:
		current_user.setPassword(pwform.vars.password)

	return dict(unform=unform, pwform = pwform)

def login():
	if current_user == None:
		form = SQLFORM.factory(
			Field('username', length=128, default=''),
			Field('password', 'password', length=64),
			submit_button='Login'
			)
		if form.process().accepted:
			if users.login(form.vars.username, form.vars.password, db, session):
				if session.back:
					# Extract session.back and clear it. Redirect to wherever the user was.
					tmp = session.back
					session.back = None
					redirect(tmp)
				else:
					# Redirect to home as fallback.
					redirect(URL(c='default', f='index'))
			else:
				response.flash = "Invalid credentials."
		return dict(form=form)
	else:
		# This should never happen, redirect them home if it does.
		redirect(URL(c='default', f='index'))

def logout():
	if current_user != None:
		users.deauth(session)
	redirect(URL(c='default', f='index'))

def register():
	if current_user == None:
		form = SQLFORM.factory(db.User, 
			Field('cpassword', 'password', 
			label="Confirm Password",
			requires=IS_EQUAL_TO(request.vars.password, error_message='Passwords do not match.')),
		    submit_button='Register'
			)
		if form.process().accepted:
			# Register the new user.
			users.register(form.vars.username, form.vars.password, db)
			# Log them in.
			users.login(form.vars.username, form.vars.password, db, session)
			redirect(URL(c='default', f='index'))
		return dict(form=form)
	else:
		redirect(URL(c='default', f='index'))
