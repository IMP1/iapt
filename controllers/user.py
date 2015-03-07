def login():
	if current_user == None:
		form = SQLFORM.factory(
			Field('username', length=128, default=''),
			Field('password', 'password', length=64)
			)
		if form.process().accepted:
			users.login(form.vars.username, form.vars.password, db, session)
			redirect(URL(c='default', f='index'))
		return dict(form=form)
	else:
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
