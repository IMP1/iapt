def index():
	if request.vars.searchterm == None:
		session.flash = "Please enter a term"
		redirect(URL(c='default', f='index'))
	results = projects.search_results(db, request.vars.searchterm)
	resultnum = len(results)
	resulttext = " results"
	if resultnum == 1:
		resulttext = " result"
	term = request.vars.searchterm
	request.vars.searchterm == None
    #Returns search results as well as the number of results
	return dict(resultnum=resultnum, results=results, term=term, resulttext=resulttext)