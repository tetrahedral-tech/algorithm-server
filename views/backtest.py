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
	balance = 200 # love money $$
	strength_to_usd = 25
	start_balance = balance
	shares = 0

	for price in enumerate(prices):
		try:
			singal, strength = algorithm_output(algorithm, prices[0:price[0]])
			usd_amount = strength * strength_to_usd
			shares_amount = usd_amount / price[1]

			if singal == 'buy' and balance >= usd_amount:
				outputs.append((price[1], (singal, strength)))
				balance -= usd_amount
				shares += shares_amount

			elif singal == 'sell' and shares >= shares_amount:
				outputs.append((price[1], (singal, strength)))
				balance += usd_amount
				shares -= shares_amount
		
		except IndexError:
			pass
	
	return {
		'outputs': outputs, 
		'algorithm': algorithm,  
		'balance': balance, 
		'start_balance': start_balance,
		'total_balance': balance + shares * price[1],
		'strength_to_usd': strength_to_usd, 
		'shares': shares, 
		'last_price': price[1], 
		'interval': interval,
		'win/lose': (balance + shares * price[1]) - start_balance ,
		'times_traded': len(outputs)
		}
