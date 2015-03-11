# -*- coding: utf-8 -*-

def index():
    response.title = "IAPT Group Six"
    return dict(projects=projects.recent_projects(db))