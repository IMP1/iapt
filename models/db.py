# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.db')

#User
db.define_table('User',
    Field('username', length=128, default='', unique=True,
        requires=[IS_NOT_EMPTY(), IS_LENGTH(128),
        IS_NOT_IN_DB(db, 'User.username' , error_message='Sorry! This username is in use.')]),
    Field('password', 'password', length=64, readable=False,
        requires=[IS_NOT_EMPTY(), IS_LENGTH(64)]),
)

statuses = ('Open', 'Closed')
#Project
db.define_table('Project',
    Field('creator', db.User),
    )

# What about document image statuses... How do these relate to project statuses?
# Can project status be derived from document image statuses?