def index():
	#Create forms to change the current user's username or password
	auth_required('You must be logged in to see your profile.')
<<<<<<< HEAD
=======
	print IS_FLOAT_IN_RANGE(0, 100, dot=".", error_message='too small or too large!')
	# Create form to change username
>>>>>>> 56858f0d9e1be5565d17412cba3651d72b964b10
	unform = SQLFORM.factory(
		Field('username', length=128, label="New Username", 
			default='', requires=[users.IS_NOT_IN_USE(db)]),
		submit_button='Change Username')
	#Change username if form is accepted
	if unform.process().accepted:
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
	if pwform.process().accepted:
		current_user.setPassword(pwform.vars.password)
<<<<<<< HEAD
	return dict(unform=unform, pwform = pwform)
=======
	# Return username and password forms to view
	return dict(unform=unform, pwform=pwform)
>>>>>>> 56858f0d9e1be5565d17412cba3651d72b964b10

def login():
	# Create login form if there is no user currently logged in
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
	# Logout the current user and return to homepage
	if current_user != None:
		users.deauth(session)
	redirect(URL(c='default', f='index'))

def register():
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
			redirect(URL(c='default', f='index'))
		return dict(form=form)
	else:
		# This should never happen, redirect them home if it does.
		redirect(URL(c='default', f='index'))
