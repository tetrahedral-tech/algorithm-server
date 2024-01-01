#Run using python unisttest tests.test_app.py
import unittest, utils

class TestApp(unittest.TestCase):

	#Test utils.py
	def test_utils(self):
		#Test if bollinger_bands in get algorithms (True)
		self.assertTrue('bollinger_bands' in utils.get_algorithms())
		#Test if bollinger_bands returns TypeError if given a non-numpy list type
		self.assertRaises(TypeError, utils.algorithm_output, 'bollinger_bands', [1, 2, 3], backtest=True)