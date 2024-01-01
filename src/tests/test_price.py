from price import *
import unittest

class TestApp(unittest.TestCase):
	#Test price.py
	def test_price(self):
		#Test is supported interval function in price.py using 240 interval (supported)
		self.assertTrue(is_supported_interval(240))
		#Test is cached interval function in price.py using 240 interval (supported)
		self.assertTrue(is_cached_interval(240))
		#Test set deafult interval using 240 (returns 240)
		self.assertEqual(set_default_interval(240), 240)
		#Test get default interval using 240 (change if the default interval is changed)
		self.assertEqual(get_default_interval(), 240)
		#Test get prices using is not none
		self.assertIsNotNone(get_prices())
		#Test get cached prices using is not none
		self.assertIsNotNone(get_cached_prices())
		#Test update cached prices using is none
		self.assertIsNone(update_cached_prices(log=False))  #log is set to False so getting cached print dont get displayed
