# Models are executed on every request. This file contains things we want
# We can import our custom modules. And make sure we track changes.
# Do not poke session.flash here, or it'll be gone.
from gluon.custom_import import track_changes
track_changes(True)

import users
import documents
import projects
import sections
import transcriptions

# Auth a user. 
current_user = users.auth(session, db)

def auth_required(msg='You must be logged in to see this page.'):
	if current_user == None:
		session.back = URL(args=request.args, host=True)
		session.flash = msg
		redirect(URL(c='user', f='login'))