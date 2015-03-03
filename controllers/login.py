def index():
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
