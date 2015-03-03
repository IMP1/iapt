# Models are executed on every request. This file contains things we want
# We can import our custom modules. And make sure we track changes.
from gluon.custom_import import track_changes
track_changes(True)

import users
import projects
import documents

# Auth a user. 
current_user = users.auth(session, db)