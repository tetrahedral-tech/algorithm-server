from importlib import import_module

def algorithm_output(algorithm, prices):
	module = import_module(f'algorithms.{algorithm}')
	signal, strength = module.signal(prices, module.algorithm(prices))

	return algorithm, (signal, strength)