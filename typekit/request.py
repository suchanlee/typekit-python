import urllib

import requests

from _version import __version__


def make_request(method, url, params=None):

	user_agent = 'Python Typekit API Wrapper v{}'.format(__version__)
	headers = { 'User-Agent' : user_agent }

	if params is not None:
		data = urllib.urlencode(params, True)
		print data

	if method == 'GET':
		res = requests.get(url, headers=headers)

	elif method == 'POST':
		res = requests.post(url, data=data, headers=headers)

	elif method == 'DELETE':
		res = requests.delete(url, data=data, headers=headers)

	return res.json()

