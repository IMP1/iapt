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

#Project
db.define_table('Project',
    Field('creator', db.User),
    Field('title', length=128),
    Field('open', 'boolean')
    )

#Document
db.define_table('Document',
	Field('project', db.Project),
	Field('image', 'upload'),
	Field('title'),
	)

#Section
db.define_table('Section',
	Field('project', db.Project),
	Field('title'),
	Field('blurb')
	)

#Transcription
db.define_table('Transcription',
	Field('section', db.Section),
	Field('document', db.Document),
	Field('text', 'string'),
	Field('accepted', 'boolean')
	)
