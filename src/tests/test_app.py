#Run using python unisttest tests.test_app.py
import unittest
import price, utils, app, time

class TestApp(unittest.TestCase):

	def test_app(self):
		application = app.app
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

			#Test internal checker authorization and results
			authorization_data = {
			  'Authorization':
			    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2ZXIiOiJzZXJ2ZXIiLCJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.RuVgthZMSmoZQHuDVPioxWm6J8MjubpJXTbxamhAU44'
			}
			internal_checker_response = app_client.get('/internal_checker', headers=authorization_data)
			self.assertEqual(internal_checker_response.status_code, 200)
			for algorithm in utils.get_algorithms():
				self.assertIn(algorithm, internal_checker_response.json['algorithms'])

			#Check internal checker response to false
			internal_checker_response = app_client.get('/signals', headers={'not_correct': 'not_correct'})
			self.assertEqual(internal_checker_response.status_code, 401)
