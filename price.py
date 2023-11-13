import numpy as np
from requests import post

def get_prices(address=None, duration='YEAR'):
	query = {
	  'operationName':
	    'TokenPrice',
	  'variables': {
	    'chain': 'ETHEREUM',
	    'duration': duration
	  },
	  'query':
	    'query TokenPrice($chain: Chain!, $address: String = null, $duration: HistoryDuration!) {\n  token(chain: $chain, address: $address) {\n    market(currency: USD) {\n      price {\n        value\n      }\n      priceHistory(duration: $duration) {\n        value\n      }\n    }\n  }\n}'
	}

	if address:
		query['variables']['address'] = address

	prices = post('https://api.uniswap.org/v1/graphql', json=query, headers={'Origin': 'http://localhost:80'}).json()
	prices = prices['data']['token']['market']

	current = float(prices['price']['value'])
	prices = [float(point['value']) for point in prices['priceHistory']]

	return np.array([current, *prices])
