def index():
	response.title = 'Search'
	if request.vars.searchterm == None or request.vars.searchterm == "":
		session.flash = "Please enter a term"
		redirect(URL(c='default', f='index'))
	results = documents.search_results(db, request.vars.searchterm)
	resultnum = len(results)
	resulttext = " Results"
	if resultnum == 1:
		resulttext = " Result"
	term = request.vars.searchterm
	request.vars.searchterm == None
    #Returns search results as well as the number of results
	return dict(resultnum=resultnum, results=results, term=term, resulttext=resulttext)