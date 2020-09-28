def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	body = [bytes(i + '\n', 'ascii') for i in environ['QUERY_STRING'].split('&')]
	return body
