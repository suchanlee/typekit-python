import copy

from .request import make_request
from .exceptions import NoKitFoundException, NoFontFoundException

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


	def get_kit(self, kit_id):
		"""
		Returns an existing kit of given id (including unpublished ones)
		"""
		url = self.build_url('get', kit_id=kit_id)
		kit = make_request('GET', url)
		if 'errors' in kit:
			raise NoKitFoundException(value='Kit with id "{}" does not exist'.format(kit_id))

		return kit


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
				if 'id' not in family:
					raise TypeError('the "id" key is required for families')
				params['families[{}][id]'.format(idx)] = family.get('id')

				if 'variations' in family:
					params['families[{}][variations]'.format(idx)] = family.get('variations')

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
		"""
		Completely replaces the existing value with the new value during POST request (Typekit spec)
		"""
		return self.modify_kit(kit_id=kit_id, name=name, domains=domains, families=families, badge=badge)


	def create_kit(self, name, domains, families=None, badge=False):
		"""
		Creates an existing kit
		"""
		return self.modify_kit(name=name, domains=domains, families=families, badge=badge)


	def remove_kit(self, kit_id):
		"""
		Removes an existing kit.
		"""
		url = self.build_url('delete', kit_id=kit_id)
		return make_request('DELETE', url, {})


	def publish_kit(self, kit_id):
		"""
		Publishes an existing kit.
		"""
		url = self.build_url('publish', kit_id=kit_id)
		return make_request('POST', url, {})


	def get_font_family(self, font):
		"""
		Retrieves font information from Typekit.
		Can use either font_slug or font_id. The font slug must
		be a slug for it to work, so slugify your input before using it.
		"""
		url = self.build_url('families', font=font)
		font_response = make_request('GET', url)

		if 'errors' in font_response:
			raise NoFontFoundException('Font "{}" does not exist'.format(font))

		return font_response


	def get_font_variations(self, font):
		"""
		Retrieves all variations of the font family.
		If font does not exist, returns False
		"""
		font_json = self.get_font_family(font)

		variations = []
		for var in font_json.get('family').get('variations'):
			variations.append(var.get('fvd'))

		return variations


	def kit_contains_font(self, kit_id, font):
		"""
		Checks to see if a font exists in a kit.
		If it does, returns True.
		If the kit does not exist or the font does not exist, returns None.
		Else, return False.
		"""
		kit_fonts = self.get_kit_fonts(kit_id)

		if len(kit_fonts) == 0:
			return False

		font = self.get_font_family(font)

		if font.get('family').get('id') in kit_fonts:
			return True

		return False


	def kit_add_font(self, kit_id, font, variations=None):
		"""
		Adds a font to a given kit.
		Font is a string.
		Variations is an optional tuple. Add only valid variations. If
		variations is not given, adds all variations (default behavior).

		If font exists in kit, returns without doing anything.
		Else, adds font to kit, returns.
		"""
		if self.kit_contains_font(kit_id, font):
			print 'Font already in kit'
			return

		new_font_family = {'id' : font}

		# add only the valid variations
		if variations is not None:
			font_avail_vars = self.get_font_variations(font)
			new_vars = []
			for var in variations:
				if var in font_avail_vars:
					new_vars.append(var)

			if len(new_vars) > 0:
				new_font_family['variations'] = ','.join(new_vars)

		kit = self.get_kit_vals(kit_id)
		kit[3].append(new_font_family)

		self.update_kit(kit_id, name=kit[0], domains=kit[1], badge=kit[2], families=kit[3])


	def kit_remove_font(self, kit_id, font):
		"""
		Removes a font from a given kit.
		Font is a string.

		If font does not exist in kit, returns without doing anything.
		Else, removes font to kit, returns.
		"""
		if not self.kit_contains_font(kit_id, font):
			print 'Font not in kit. Nothing to remove.'
			return

		kit = self.get_kit_vals(kit_id)
		font_data = self.get_font_family(font)
		font_id = font_data.get('family').get('id')

		for idx, family in enumerate(kit[3]):
			if font_id == family.get('id'):
				kit[3].pop(idx)

		self.update_kit(kit_id, name=kit[0], domains=kit[1], badge=kit[2], families=kit[3])


	def get_kit_vals(self, kit_id):
		"""
		Retrieves kit vals in a list of format: [name, domains, families, badge]
		"""
		kit = self.get_kit(kit_id).get('kit')
		families = []
		for f in kit.get('families'):
			family_dict = {
				'id' : f.get('id'),
				'variations' : ','.join(f.get('variations'))
			}
			families.append(family_dict)

		return [kit.get('name'), kit.get('domains'), kit.get('badge'), families]


	def get_kit_fonts(self, kit_id):
		"""
		Retrieves a list of font ids in a given kit
		Returns None if kit does not exist
		Returns an empty list if no fonts in kit
		"""
		kit = self.get_kit(kit_id)
		return [family.get('id') for family in kit.get('kit').get('families')]


	def build_url(self, method, kit_id=None, font=None):
		url = self.scheme + self.host

		if method == 'list' or method == 'create':
			url += 'kits'

		if method == 'get' or method == 'update' or method == 'delete':
			url += 'kits/{}'.format(kit_id)

		if method == 'publish':
			url += 'kits/{}/publish'.format(kit_id)

		if method == 'families':
			url += 'families/{}'.format(font)

		url += '?token={}'.format(self.api_token)
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


