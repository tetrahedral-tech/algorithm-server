from price import get_prices, get_default_interval, get_cached_prices, is_cached_interval, is_supported_interval
from importlib import import_module
from utils import get_algorithms
from flask import request

def algorithm_output(algorithm, prices):
	module = import_module(f'algorithms.{algorithm}')
	signal, strength = module.signal(prices, module.algorithm(prices))
	return signal, strength

def backtest(algorithm):
	default_interval = get_default_interval()
	interval = int(request.args.get('interval') or default_interval)
	algorithms = ['price', *get_algorithms()]

	if interval and is_cached_interval(interval):
		prices, timestamps, _ = get_cached_prices(interval=interval)
	elif interval and is_supported_interval(interval):
		prices, timestamps, _ = get_prices(interval=interval)
	elif not interval:
		prices, timestamps, _ = get_cached_prices()
	else:
		return 'Unsupported Interval', 400

	if algorithm not in algorithms:
		return 'Unsupported Algorithm', 404	

	outputs = []
	strength_to_usd = 25
	money = 200 #love fake money
	start_money = money
	shares = 0

	for price in enumerate(prices):
		try:
			singal, strength = algorithm_output(algorithm, prices[0:price[0]])
			usd_amount = strength * strength_to_usd
			shares_amount = usd_amount / price[1]

			if singal == 'buy' and money >= usd_amount:
				outputs.append({price[1]: (singal, strength)})
				money -= usd_amount
				shares += shares_amount

			elif singal == 'sell' and shares >= shares_amount:
				outputs.append({price[1]: (singal, strength)})
				money += usd_amount
				shares -= shares_amount
		
		except IndexError:
			pass
	
	money += shares * price[1]	
	return f'<center><h1>trades</h1>{outputs}</center>, <center><h1>Earnings</h1><h2>{money-start_money}</h2></center>'