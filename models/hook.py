# Models are executed on every request. This file contains things we want
# We can import our custom modules here, note that web2py caches modules.
import users
import projects
import documents

print users.auth(session, db)