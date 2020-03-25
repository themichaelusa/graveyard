import time
import ciso8601
import requests
import pandas as pd
from realtime_talib import Indicator
import matplotlib.pyplot as plt

class Pipeline(object):

	def __init__(self, interval): 

		self.interval = interval
		self.POLO_URL = 'https://poloniex.com/public'
		self.POLO_HIST_DATA = self.POLO_URL + '?command=returnChartData&currencyPair={}&start={}&end={}&period={}'

	def dateToUNIX(self, date): #format: "YYYYMMDD hhmmss"
		ts = ciso8601.parse_datetime(date)
		return time.mktime(ts.timetuple())

	def getCryptoHistoricalData(self, currencyPair, startDate, endDate):

		stDateUNIX = self.dateToUNIX(startDate)
		eDateUNIX = self.dateToUNIX(endDate)
		poloniexJsonURL = self.POLO_HIST_DATA.format(currencyPair, stDateUNIX, eDateUNIX, self.interval)
		poloniexJson = requests.get(poloniexJsonURL).json()

		histDataframe = pd.DataFrame.from_records(poloniexJson)
		histDataframe.drop('quoteVolume', axis=1, inplace=True)
		histDataframe.drop('weightedAverage', axis=1, inplace=True)
		histDataframe['date'] = histDataframe['date'].astype(float)

		return histDataframe[["date", "open", "high", "low", "close", "volume"]]

newPL = Pipeline(300)
OHLCV = newPL.getCryptoHistoricalData('USDT_BTC', '20170122', '20170823')
BBANDS = Indicator(OHLCV, 'BBANDS', 10, 2, 2, 1)
upper, ema, lower = BBANDS.getHistorical(lag=150)
print(len(upper), len(ema), len(lower))
price, date = OHLCV['open'], OHLCV['date']
plt.plot(price[61331], upper[9198449:9198599], ema[9198449:9198599], lower[9198449:9198599])






