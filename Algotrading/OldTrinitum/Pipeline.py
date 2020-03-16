
import time
import json
import requests
import Utilities as utl
import pandas as pd
import numpy as np

class Pipeline(object):

	def __init__(self, interval): 

		self.interval = interval
		self.POLO_URL = 'https://poloniex.com/public'
		self.POLO_HIST_DATA = self.POLO_URL + '?command=returnChartData&currencyPair={}&start={}&end={}&period={}'

	def getCryptoHistoricalData(self, currencyPair, startDate, endDate):

		stDateUNIX = utl.dateToUNIX(startDate)
		eDateUNIX = utl.dateToUNIX(endDate)
		poloniexJsonURL = self.POLO_HIST_DATA.format(currencyPair, stDateUNIX, eDateUNIX, self.interval)
		poloniexJson = requests.get(poloniexJsonURL).json()

		histDataframe = pd.DataFrame.from_records(poloniexJson)
		histDataframe.drop('quoteVolume', axis=1, inplace=True)
		histDataframe.drop('weightedAverage', axis=1, inplace=True)
		histDataframe['date'] = histDataframe['date'].astype(float)

		return histDataframe[["date", "open", "high", "low", "close", "volume"]]

class Formatter(object):

	def __init__(self): pass

	def formatSpotData(self, sdDict):
		return [float(sdDict['price']), float(sdDict['volume'])]

	def formatTechIndicators(self, tiDict):
		
		dictVals = list(tiDict.values())
		dictVals = dictVals[:len(dictVals)-1] #removes rethinkDB ID
		return utl.flattenList(dictVals)

	def dfToHeikenAshi(self, dataframe): pass

def indsToDF(inds):
	techDF = [pd.Dataframe()]
	return techDF
