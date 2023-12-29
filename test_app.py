import unittest
import price, utils, backtest_module, app

class TestApp(unittest.TestCase):
	#Test price.py
	def test_price(self):
		#Test is supported interval function in price.py using 240 interval (supported)
		self.assertTrue(price.is_supported_interval(240))
		#Test is cached interval function in price.py using 240 interval (supported)
		self.assertTrue(price.is_cached_interval(240))
		#Test set deafult interval using 240 (returns 240)
		self.assertEqual(price.set_default_interval(240), 240)
		#Test get default interval using 240 (change if the default interval is changed)
		self.assertEqual(price.get_default_interval(), 240)
		#Test get prices using is not none
		self.assertIsNotNone(price.get_prices())
		#Test get cached prices using is not none
		self.assertIsNotNone(price.get_cached_prices()) 
		#Test update cached prices using is none
		self.assertIsNone(price.update_cached_prices(log=False)) #log is set to False so getting cached print dont get displayed

	#Test utils.py
	def test_utils(self):
		#Test if bollinger_bands in get algorithms (True)
		self.assertTrue('bollinger_bands' in utils.get_algorithms())
		#Test if bollinger_bands returns TypeError if given a non-numpy list type
		self.assertRaises(TypeError ,utils.algorithm_output, 'bollinger_bands', [1,2,3], backtest=True)	

	#Test backtest_module.py
	def test_backtest(self):
		backtest_data = backtest_module.backtest('bollinger_bands', price.get_prices()[0])
		#Test back test data keys are correct and backtest data exsits
		backtest_dict = { 
      'transactions': [], 
      'algorithm': 'bollinger_bands', 
      'balance':1, 'start_balance':1, 
      'final_total':1, 
      'strength_to_usd':1, 
      'shares':1, 
      'profit':1, 
      'profit_percentage %':1 
    }
		self.assertIsNotNone(backtest_data)
		self.assertCountEqual(backtest_dict.keys(), backtest_data.keys())
		#Test transactions keys are correct and and transactions exsits
		transactions_dict = {'price': price, 'signal': 'signal', 'strength': 1, 'current_balance': 1, 'current_shares': 1}
		transactions = backtest_data['transactions'][0] #take the first transaction of transactions list
		self.assertIsNotNone(transactions_dict)
		self.assertCountEqual(transactions_dict.keys(), transactions.keys())
		#Test if algorithm is correct (using bollinger bands change whenever needed) and algorithm variable exsits
		self.assertIsNotNone(backtest_data['algorithm'])
		self.assertEqual('bollinger_bands', backtest_data['algorithm'])
		#Test if start_balance is greater than 0 and exsits
		self.assertIsNotNone(backtest_data['start_balance'])
		self.assertGreater(backtest_data['start_balance'], 0)
		#Test if strength_to_usd is greater than 0 and exsits
		self.assertIsNotNone(backtest_data['strength_to_usd'])
		self.assertGreater(backtest_data['strength_to_usd'], 0)
		#Test if all of these keys are inegers and exsits (raises error if nan)
		self.assertTrue(type(backtest_data['balance']), int)
		self.assertTrue(type(backtest_data['final_total']), int)
		self.assertTrue(type(backtest_data['shares']), int)
		self.assertTrue(type(backtest_data['profit']), int)
		self.assertTrue(type(backtest_data['profit_percentage %']), int)

	def test_backtest_plot(self):
		backtest_plot_data = backtest_module.backtest('bollinger_bands', price.get_prices()[0], plot=True)
		#Test back test data keys are correct and backtest data exsits
		backtest_dict = { 
      'transactions': [], 
      'algorithm': 'bollinger_bands', 
      'balance':1, 'start_balance':1, 
      'final_total':1, 
      'strength_to_usd':1, 
      'shares':1, 
      'profit':1, 
      'profit_percentage %':1 
    }
		self.assertIsNotNone(backtest_plot_data)
		self.assertCountEqual(backtest_dict.keys(), backtest_plot_data.keys())
		#Test if backtest plot exsits and not raising any errors
		backtest_plot = backtest_module.plot(backtest_plot_data)
		self.assertIsNotNone(backtest_plot)

	def test_views(self):
		application = app.get_app()
		app_client = application.test_client()
		intervals = price.supported_intervals
		algorithms = utils.get_algorithms()
		#Test backtest && backtest plot && plot views
		for algorithm in algorithms:
			for interval in intervals:
				#fully test backtest_response
				backtest_response = app_client.get(f'/backtest/{algorithm}?interval={interval}')
				self.assertEqual(backtest_response.status_code, 200)
				self.assertIn(b'transactions', backtest_response.data)
				self.assertIn(b'algorithm', backtest_response.data)
				self.assertIn(b'balance', backtest_response.data)
				self.assertIn(b'start_balance', backtest_response.data)
				self.assertIn(b'final_total', backtest_response.data)
				self.assertIn(b'strength_to_usd', backtest_response.data)
				self.assertIn(b'shares', backtest_response.data)
				self.assertIn(b'profit', backtest_response.data)
				self.assertIn(b'profit_percentage %', backtest_response.data)
				#test backtest_plot_response	
				backtest_plot_response = app_client.get(f'/backtest/{algorithm}?interval={interval}')
				self.assertEqual(backtest_plot_response.status_code, 200)
				#test plot_response
				plot_response = app_client.get(f'/backtest/{algorithm}?interval={interval}')
				self.assertEqual(plot_response.status_code, 200)



if __name__ == '__main__':
	unittest.main()