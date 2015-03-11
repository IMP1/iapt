# -*- coding: utf-8 -*-

def index():
	# Title the page and return the 9 most recent projects to the view
    response.title = "IAPT Group Six"
    return dict(projects=projects.recent_projects(db))