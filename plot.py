import numpy as np
import matplotlib.pyplot as plt
from price import get_prices
from algorithms.bollinger_bands import algorithm as boillinger_bands
from algorithms.rsi import algorithm as rsi
from algorithms.macd import algorithm as macd

# @TODO split plotting off into another algorithm function. def plot(subplot, prices, data)

prices = get_prices('ETH/USD', interval=1440)

upper_band, lower_band, middle_band = boillinger_bands(prices)
rsi_data = rsi(prices)
macd, signal = macd(prices)

bb_indicies = np.arange(0, upper_band.shape[0])
rsi_indicies = np.arange(0, rsi_data.shape[0])
macd_indicies = np.arange(0, macd.shape[0])

## Boillinger Bands
plt.subplot(221)

bb_sliced_prices = prices[:upper_band.shape[0]]
plt.fill_between(bb_indicies, upper_band, lower_band, color='grey', alpha=0.3)

# Price/SMA
plt.plot(bb_indicies, bb_sliced_prices, color='plum')
plt.plot(bb_indicies, middle_band, color='mediumpurple')

# Buy/Sell Signals
bb_upper_condition = bb_sliced_prices >= upper_band
bb_lower_condition = bb_sliced_prices <= lower_band

plt.scatter(bb_indicies[bb_upper_condition], bb_sliced_prices[bb_upper_condition], color='lightcoral')
plt.scatter(bb_indicies[bb_lower_condition], bb_sliced_prices[bb_lower_condition], color='darkturquoise')

## RSI
plt.subplot(222)
plt.plot(rsi_indicies, rsi_data, color='plum')

# Thresholds
rsi_upper = np.full(rsi_data.shape, 70)
rsi_lower = np.full(rsi_data.shape, 30)

plt.fill_between(rsi_indicies, rsi_upper, rsi_lower, color='grey', alpha=0.3)
plt.plot(rsi_indicies, rsi_upper, linestyle='dashed', color='lightcoral')
plt.plot(rsi_indicies, rsi_lower, linestyle='dashed', color='darkturquoise')

## MACD
plt.subplot(223)

macd_upper_condition = macd > signal
macd_lower_condition = macd < signal

plt.scatter(macd_indicies[macd_upper_condition], signal[macd_upper_condition], color='darkturquoise')
plt.scatter(macd_indicies[macd_lower_condition], signal[macd_lower_condition], color='lightcoral')

plt.plot(signal, color='plum')
plt.plot(macd, color='mediumpurple')

plt.show()
