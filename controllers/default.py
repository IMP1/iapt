# -*- coding: utf-8 -*-

def index():
	# Title the page and return the 9 most recent documents to the view
    response.title = 'Home'
    return dict(recents=documents.recent_documents(db))