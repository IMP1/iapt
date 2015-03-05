def login():
	if current_user == None:
		form = SQLFORM.factory(
			Field('username', length=128, default=''),
			Field('password', 'password', length=64)
			)
		if form.process().accepted:
			users.login(form.vars.username, form.vars.password, db, session)
		return dict(form=form)
	else:
		redirect(URL(c='default'))

def logout():
	if current_user != None:
		users.deauth(session)
	redirect(URL(c='default'))

def register():
	if current_user == None:
		form = SQLFORM.factory(db.User, 
			Field('cpassword', 'password', 
			label="Confirm",
			requires=IS_EQUAL_TO(request.vars.password, error_message='Passwords do not match.')),
		    submit_button='Next >'
			)
		if form.process().accepted:
			users.login(form.vars.username, form.vars.password, db, session)
		return dict(form=form)
	else:
		redirect(URL(c='default'))
