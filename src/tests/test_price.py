from price import *
import unittest

class TestApp(unittest.TestCase):
	#Test price.py
	def test_price(self):
		#Test is supported interval function in price.py using 240 interval (supported)
		self.assertTrue(is_supported_interval(240))
		#Test set deafult interval using 240 (returns 240)
		self.assertEqual(set_default_interval(240), 240)
		#Test get default interval using 240 (change if the default interval is changed)
		self.assertEqual(get_default_interval(), 240)
		#Test get prices using is not none
		self.assertIsNotNone(get_prices())
