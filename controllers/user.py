def index():
	response.title = 'Your Profile'
	#Create forms to change the current user's username or password
	auth_required('You must be logged in to see your profile.')
	# Create form to change username
	unform = SQLFORM.factory(
		Field('username', length=128, label="New Username", 
			default='', requires=[users.IS_NOT_IN_USE(db), IS_NOT_EMPTY()]),
		submit_button='Change Username')
	#Change username if form is accepted
	if unform.process(message_onsuccess={'msg': 'Username changed!', 'class': 'success_flash'}).accepted:
		current_user.setUsername(request.vars.username)
	# Create form to change password
	pwform = SQLFORM.factory(
		Field('password', 'password', length=64, label="New Password"),
		Field('cpassword', 'password', 
			label="Confirm Password",
			requires=IS_EQUAL_TO(request.vars.password, error_message='Passwords do not match.')),
		submit_button='Change Password'
		)
	#Change password if form is accepted
	if pwform.process(message_onsuccess={'msg': 'Password changed!', 'class': 'success_flash'}).accepted:
		current_user.setPassword(pwform.vars.password)
	# Return username and password forms to view
	return dict(unform=unform, pwform=pwform)

def login():
	response.title = 'Login'
	# Create login form if there is no user currently logged in
	if current_user == None:
		form = SQLFORM.factory(
			Field('username', length=128, default=''),
			Field('password', 'password', length=64),
			submit_button='Login'
			)
		if form.process().accepted:
			if users.login(form.vars.username, form.vars.password, db, session):
				session.flash = {'msg': 'You have been logged in.', 'class': 'success_flash'}
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
	# Logout the current user and return to homepage
	if current_user != None:
		session.flash = {'msg': 'You have been logged out.', 'class': 'success_flash'}
		users.deauth(session)
	redirect(URL(c='default', f='index'))

def register():
	response.title = 'Register'
	# Create register form if there is no user currently logged in
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
			session.flash = {'msg': 'You have succesfully registered!', 'class': 'success_flash'}
			redirect(URL(c='default', f='index'))
		return dict(form=form)
	else:
		# This should never happen, redirect them home if it does.
		redirect(URL(c='default', f='index'))
