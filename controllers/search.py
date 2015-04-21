def index():
	# Title the page
	response.title = 'Search'
	# Handle blank input
	if request.vars.searchterm == None or request.vars.searchterm == "":
		session.flash = "Please enter a term"
		redirect(request.env.http_referer)
	# Get results from db
	results = documents.search_results(db, request.vars.searchterm)
	# Calculate number of results
	resultnum = len(results)
	# Create result(s) text
	resulttext = " Results"
	if resultnum == 1:
		resulttext = " Result"
	term = request.vars.searchterm
	# Clear search term
	request.vars.searchterm == None
	# Return search results as well as the number of results
	return dict(resultnum=resultnum, results=results, term=term, resulttext=resulttext)