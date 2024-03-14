#Run using python unisttest tests.test_app.py
import unittest
import price, backtest_module

class TestApp(unittest.TestCase):
	#Test backtest_module.py, using backtest plot data is because theres no much diffirence (optomization)
	def test_backtest(self):
		prices, timestamps = price.get_prices(240, 'USDC-WETH')
		backtest_plot_data = backtest_module.backtest('bollinger_bands', prices, timestamps, plot=True)
		#Test back test data keys are correct and backtest data exsits
		backtest_dict = {
		  'transactions': [],
		  'algorithm': 'bollinger_bands',
		  'balance': 1,
		  'start_balance': 1,
		  'final_total': 1,
		  'strength_to_usd': 1,
		  'shares': 1,
		  'profit': 1,
		  'profit_percentage %': 1
		}

		self.assertIsNotNone(backtest_plot_data)
		self.assertCountEqual(backtest_dict.keys(), backtest_plot_data.keys())
		#Test transactions keys are correct and and transactions exsits

		backtest_plot = backtest_module.plot(backtest_plot_data)
		self.assertIsNotNone(backtest_plot)

		transactions_dict = {
		  'price': price,
		  'signal': 'signal',
		  'strength': 1,
		  'current_balance': 1,
		  'current_shares': 1,
		  'timestamp': 1
		}

		transactions = backtest_plot_data['transactions'][0]  #take the first transaction of transactions list
		self.assertIsNotNone(transactions_dict)
		self.assertCountEqual(transactions_dict.keys(), transactions.keys())
		#Test if algorithm is correct (using bollinger bands change whenever needed) and algorithm variable exsits
		self.assertIsNotNone(backtest_plot_data['algorithm'])
		self.assertEqual('bollinger_bands', backtest_plot_data['algorithm'])
		#Test if start_balance is greater than 0 and exsits
		self.assertIsNotNone(backtest_plot_data['start_balance'])
		self.assertGreater(backtest_plot_data['start_balance'], 0)
		#Test if strength_to_usd is greater than 0 and exsits
		self.assertIsNotNone(backtest_plot_data['strength_to_usd'])
		self.assertGreater(backtest_plot_data['strength_to_usd'], 0)
		#Test if all of these keys are inegers and exsits (raises error if nan)
		self.assertTrue(type(backtest_plot_data['balance']), int)
		self.assertTrue(type(backtest_plot_data['final_total']), int)
		self.assertTrue(type(backtest_plot_data['shares']), int)
		self.assertTrue(type(backtest_plot_data['profit']), int)
		self.assertTrue(type(backtest_plot_data['profit_percentage %']), int)
