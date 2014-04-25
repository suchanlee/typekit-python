
from request import make_request

import pdb

class Typekit(object):

	use_ssl = True
	host = 'typekit.com/api/v1/json/'


	def __init__(self, **kwargs):
		self.use_ssl = kwargs.get('use_ssl', self.use_ssl)
		self.host = kwargs.get('host', self.host)
		self.scheme = self.use_ssl and 'https://' or 'http://'
		self.default_domains = ['localhost']

		self.api_token = kwargs.get('api_token', None)

		if 'api_token' not in kwargs:
			raise TypeError('The Typekit API Token must be provided')


	def list_kits(self):
		"""
		Returns a json representation of the kits associated with this
		api token
		"""
		return make_request('GET', self.build_url(method='list')).get('kits')


	def get_kit(self, kit_id=None):
		"""
		Returns an existing kit of given id (including unpublished ones)
		"""
		if kit_id is None:
			raise TypeError('Typekit kit ID is required to get existing kit')

		url = self.build_url('get', kit_id=kit_id)
		return make_request('GET', url)


	def modify_kit(self, kit_id=None, name=None, domains=None, families=None, badge=False):
		"""
		Updates or creates a new kit.
		Kwargs contains the parameters:
			name (string),
			domains (list/string),
			families
				list of dictionaries with key : values
					- 'id' : family id (string)
					- (optional) 'variations' : comma separated variations (string)
		If successful, returns True. Else, returns False
		"""
		params = {}

		if name is not None:
			params['name'] = name

		if domains is not None:
			params['domains[]'] = self.get_param_type_list(domains)
		else:
			params['domains[]'] = self.default_domains

		if families is not None:
			for idx, family in enumerate(families):
				try:
					params['families[{}][id]'.format(idx)] = family.get('id')
				except:
					raise TypeError('the "id" key is required for families')
				try:
					params['families[{}][variations]'.format(idx)] = family.get('variations')
				except:
					pass # does not pass in the variation field if it does not exist

		if not badge:
			params['badge'] = 'false'
		else:
			params['badge'] = 'true'

		if kit_id is None:
			url = self.build_url('create')
		else:
			url = self.build_url('update', kit_id=kit_id)

		return make_request('POST', url, params)


	def update_kit(self, kit_id, name=None, domains=None, families=None, badge=None):
		return self.modify_kit(kit_id=kit_id, name=name, domains=domains, families=families, badge=badge)


	def create_kit(self, name, domains, families=None, badge=False):
		"""
		Creates an existing kit
		"""
		return self.modify_kit(name=name, domains=domains, families=families, badge=badge)


	def remove_kit(self, kit_id=None):
		"""
		Removes an existing kit.
		"""
		if kit_id is None:
			raise TypeError('Typekit kit ID is required to get remove kit')

		url = self.build_url('delete', kit_id=kit_id)
		return make_request('DELETE', url, {})


	def publish_kit(self, kit_id=None):
		"""
		Publishes an existing kit.
		"""

		if kit_id is None:
			raise TypeError('Typekit kit ID is required to get publish kit')

		url = self.build_url('publish', kit_id=kit_id)
		return make_request('POST', url, {})


	def build_url(self, method, kit_id=None):
		url = self.scheme + self.host

		if method == 'list' or method == 'create':
			url += 'kits'

		if method == 'get' or method == 'update' or method == 'delete':
			url += 'kits/{}'.format(kit_id)

		if method == 'publish':
			url += 'kits/{}/publish'.format(kit_id)

		url += '?token={}'.format(self.api_token)
		print url
		return url


	def get_param_type_list(self, param, param_name=None):

		if isinstance(param, list):
			return param

		elif isinstance(param, basestring):
			return [param]

		else:
			if param_name is not None:
				error_message = '"{}" parameter must be of type list'.format(param_name)
			else:
				error_message = 'The parameter must be of type list'
			raise TypeError(error_message)


