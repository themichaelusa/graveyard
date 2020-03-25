import TradingInstance as ti
import Strategy as strat
import Utilities as utl

class TestingInstance(object):

	def __init__(self, name, capital, commission):
		
		self.name = name
		self.capital = capital
		self.commission = commission

		self.histData = cst.NOT_SET
		self.period = cst.NOT_SET
		self.histPeriod = cst.NOT_SET
		self.indicatorLag = cst.NOT_SET

		self.exchange = cst.NOT_SET
		self.symbol = cst.NOT_SET
		self.tradeQuantity = cst.NOT_SET
		self.lossTolerance = cst.NOT_SET
		self.tradeInstance = cst.NOT_SET
		self.strategy = cst.NOT_SET
		self.indicators = {}

	def setSymbol(self, exchange, symbol, period=300):

		self.exchange = exchange
		self.symbol = symbol
		self.period = period

	def addStrategy(self, stratName, entryCond, exitCond):
		self.strategy = strat.Strategy(stratName, entryCond, exitCond)

	def addIndicator(self, indName, *indArgs):
		self.indicators.update({indName: indArgs})

	def setTradeParams(self, trade_quantity=1, loss_tolerance=.05, total_positions=5):
		self.tradeQuantity, self.lossTolerance = trade_quantity, loss_tolerance
		self.totalPositions = total_positions

	def set_advanced_params(hist_period=300, indicator_lag=1):
		self.histPeriod, self.indicatorLag = hist_period, indicator_lag

	def preRunOperations(self, testType, runArgs, tradeParams):
		
		startDate, endDate, period = runArgs
		dbName = testType + startDate + endDate + str(period)
		self.tradeInstance = ti.TradingInstance(dbName, self.name)
		self.tradeInstance.setTradingParams(self.exchange, self.ticker, self.indicators, *tradeParams)
		self.tradeInstance.setHistoricalParams(self.period, self.histLag)
		self.tradeInstance.start(self.strategy, self.capital, self.commission)

class Backtest(TestingInstance):

	def __init__(self, name, capital, commission):
		super().__init__(name, capital, commission)
		self.testType = "BT"

	def run(self, startDate, endDate):

		tradeParams = (self.tradeQuantity, self.lossTolerance)
		self.preRunOperations(self.testType, (startDate, endDate, period), tradeParams)
		self.tradeInstance.run(self.testType, endDate, 1)

class PaperTrade(TestingInstance):

	def __init__(self, name, capital, commission):
		super().__init__(name, capital, commission)
		self.testType = "PT"

	def run(self, endDate, period):

		startDate = utl.getCurrentDateStr()
		tradeParams = (self.tradeQuantity, self.lossTolerance)
		self.preRunOperations(self.testType, (startDate, endDate, period), tradeParams)
		self.tradeInstance.run(self.testType, period, endDate, 1)
