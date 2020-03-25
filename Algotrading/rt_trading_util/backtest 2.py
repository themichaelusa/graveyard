import pipeline as pl
import utilities as ut
import algorithm as alg
import constants as cons
import diagnostics as diag

# TODO: Finish functions for gain, captial, and commision inclusion in Hist. backtest (Michael) 

class Backtest(object):

	def __init__(self, currency, period, capital):

		self.currency = currency
		self.period = period
		self.capital = capital

class LiveBacktest(Backtest):
	def __init__(self, currency, period, capital):
		super().__init__(currency, capital)

# TODO: Finish functions for date setting/formatting-goes into UI as well (Not assigned yet) 

class HistoricalBacktest(Backtest):

	def __init__(self, currency, period, capital, startDate, endDate):
		super().__init__(currency, period, capital)

		self.startDate = startDate
		self.endDate = endDate

		self.gainPerCent = cons.NOT_SET
		self.finishedPositions = cons.NOT_SET
		self.formattedPositions = cons.NOT_SET
		self.verifiedStats = cons.NOT_SET

	def setGain(self, gain): self.gainPerCent = gain

	def run(self):
		
		histTest = pl.Pipeline(cons.POLONIEX_PUBLIC_URL, cons.POLONIEX_HISTORICAL_DATA)
		histData = histTest.getHistoricalData(self.currency, self.period, self.startDate, self.endDate)
		laggedHistData = histTest.getHistoricalData(self.currency, (self.period * 2), self.startDate, self.endDate)
		packagedHistoricalData = histTest.packageHistoricalData(histData, laggedHistData)

		self.finishedPositions = alg.tryAlgorithmLogic(packagedHistoricalData)
		self.formattedPositions = pl.algoResultsToDataframe(self.finishedPositions[0], self.finishedPositions[1], self.gainPerCent)
		self.verifiedStats = diag.verifyBacktestAccuracy(self.formattedPositions, False)

		return diag.CMD_UI(self.verifiedStats, self.currency, ut.CURRENT_DATE)

	def diagnostics(self, toCSV):

		if (toCSV == True): 
			dataframe = self.formattedPositions[0]
			dataframe.to_csv((self.currency + '_eAlgoV1.1 Results.csv'), sep='\t')

		return diag.exportDiagnosticsPanel()

	def plot(self): 
		return diag.testPlot(self.formattedPositions)

# TODO: Research what needs to be done/finished for a live pipeline/backtest (Shovik & Michael) 

class CustomBacktest(Backtest):
	def __init__(self, strategy, data, capital, commission):

		super().__init__(capital, commission)
		self.strategy = strategy
		self.data = data

BTC = HistoricalBacktest('USDT_BTC', 900, None, '20170501', '20170607')
BTC.setGain(.01)

BTC.run()
BTC.diagnostics(True)
