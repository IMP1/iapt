# Models are executed on every request. This file contains things we want
# We can import our custom modules here, note that web2py caches modules.
from gluon.custom_import import track_changes
track_changes(True)

import users
import projects
import documents

# Auth a user.
user = users.auth(session, db)