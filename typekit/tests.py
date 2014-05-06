import unittest

from .typekit import Typekit

import pdb


class TypekitTests(unittest.TestCase):

	def setUp(self):
		self.tk = Typekit(api_token='')

	def test_list_kits(self):
		kits = self.tk.list_kits()
		self.assertTrue(type(kits) is list)
		self.assertTrue(len(kits) > 0)


	def test_kit_creation(self):
		name = 'test_kit_creation'
		domains = ['localhost', 'http://domain.com']
		families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]

		res = self.tk.create_kit(name, domains, families)
		self.assertFalse('errors' in res)

		kit = res['kit']

		self.assertFalse(kit['badge'])

		self.assertTrue('localhost' in kit['domains'])
		self.assertTrue('domain.com' in kit['domains'])
		self.assertEquals(kit['name'], name)

		family1 = kit['families'][0]
		self.assertEquals(family1['subset'], 'default')
		self.assertEquals(family1['name'], 'Futura PT')
		self.assertEquals(family1['id'], 'ftnk')
		self.assertTrue('n3' in family1['variations'])
		self.assertTrue('n4' in family1['variations'])
		self.assertEquals(len(family1['variations']), 2)

		family2 = kit['families'][1]
		self.assertEquals(family2['subset'], 'default')
		self.assertEquals(family2['name'], 'Droid Serif')
		self.assertEquals(family2['id'], 'pcpv')
		self.assertTrue('n4' in family2['variations'])
		self.assertEquals(len(family2['variations']), 1)

		self.tk.remove_kit(kit['id'])


	def test_get_kit(self):

		name = 'test_kit_creation'
		domains = ['localhost', 'http://domain.com']
		families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]

		res = self.tk.create_kit(name, domains, families)
		self.assertFalse('errors' in res)

		kit_id = res['kit']['id']

		res = self.tk.get_kit(kit_id)

		kit = res['kit']

		self.assertFalse(kit['badge'])

		self.assertTrue('localhost' in kit['domains'])
		self.assertTrue('domain.com' in kit['domains'])
		self.assertEquals(kit['name'], name)

		family1 = kit['families'][0]
		self.assertEquals(family1['subset'], 'default')
		self.assertEquals(family1['name'], 'Futura PT')
		self.assertEquals(family1['id'], 'ftnk')
		self.assertTrue('n3' in family1['variations'])
		self.assertTrue('n4' in family1['variations'])
		self.assertEquals(len(family1['variations']), 2)

		family2 = kit['families'][1]
		self.assertEquals(family2['subset'], 'default')
		self.assertEquals(family2['name'], 'Droid Serif')
		self.assertEquals(family2['id'], 'pcpv')
		self.assertTrue('n4' in family2['variations'])
		self.assertEquals(len(family2['variations']), 1)

		self.tk.remove_kit(kit_id)


	def test_get_font_family(self):
		font = self.tk.get_font_family('futura-pt')
		self.assertEquals(font['family']['id'], 'ftnk')
		self.assertEquals(font['family']['name'], 'Futura PT')


	def test_kit_contains_font(self):

		name = 'test_kit_creation'
		domains = ['localhost', 'http://domain.com']
		families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]

		res = self.tk.create_kit(name, domains, families)
		self.assertFalse('errors' in res)

		kit_id = res['kit']['id']

		self.assertTrue(self.tk.kit_contains_font(kit_id, 'ftnk'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'futura-pt'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'pcpv'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'droid-serif'))

		self.tk.remove_kit(kit_id)


	def test_kit_add_font(self):
		name = 'test_kit_creation'
		domains = ['localhost', 'http://domain.com']
		families = [{'id': 'ftnk', 'variations': 'n3,n4'}]

		res = self.tk.create_kit(name, domains, families)
		self.assertFalse('errors' in res)

		kit_id = res['kit']['id']

		self.assertTrue(self.tk.kit_contains_font(kit_id, 'ftnk'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'futura-pt'))
		self.assertFalse(self.tk.kit_contains_font(kit_id, 'pcpv'))
		self.assertFalse(self.tk.kit_contains_font(kit_id, 'droid-serif'))

		self.tk.kit_add_font(kit_id, 'pcpv', variations=['n4'])
		self.tk.publish_kit(kit_id)

		self.assertTrue(self.tk.kit_contains_font(kit_id, 'pcpv'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'droid-serif'))

		self.tk.remove_kit(kit_id)


	def test_kit_remove_font(self):
		name = 'test_kit_creation'
		domains = ['localhost', 'http://domain.com']
		families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]

		res = self.tk.create_kit(name, domains, families)
		self.assertFalse('errors' in res)

		kit_id = res['kit']['id']

		self.assertTrue(self.tk.kit_contains_font(kit_id, 'ftnk'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'futura-pt'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'pcpv'))
		self.assertTrue(self.tk.kit_contains_font(kit_id, 'droid-serif'))

		self.tk.kit_remove_font(kit_id, 'pcpv')
		self.tk.publish_kit(kit_id)

		self.assertFalse(self.tk.kit_contains_font(kit_id, 'pcpv'))
		self.assertFalse(self.tk.kit_contains_font(kit_id, 'droid-serif'))

		self.tk.remove_kit(kit_id)


	def test_get_kit_fonts(self):
		name = 'test_kit_creation'
		domains = ['localhost', 'http://domain.com']
		families = [{'id': 'ftnk', 'variations': 'n3,n4'}, {'id': 'pcpv', 'variations': 'n4'}]

		res = self.tk.create_kit(name, domains, families)
		kit_id = res['kit']['id']

		fonts = self.tk.get_kit_fonts(kit_id)
		self.assertTrue('ftnk' in fonts)
		self.assertTrue('pcpv' in fonts)
		self.assertEquals(len(fonts), 2)

		self.tk.remove_kit(kit_id)



if __name__ == '__main__':
    unittest.main()

