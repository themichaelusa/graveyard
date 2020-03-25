import rethinkdb as r
from realtime_talib import Indicator

import time
import DatabaseManager as dbm
import Strategy as stra
import Pipeline as plu
import Utilities as utl
import Constants as cst
import Position as pos
import Order as order

class TradingInstance(object):
	
	def __init__(self, dbName, runID):

		self.NONE = "None"
		self.dbName = dbName
		self.tInstID = runID

		self.ticker = None
		self.exchange = None
		self.tradeQuan = None
		self.tolerance = None
		self.techInds = None
		self.histDF = None
		
		self.conn = None
		self.dbRef = None
		self.databaseManager = None

	def initDatabase(self, hostname = "localhost", port = 28015): 

		r.db_create(self.dbName).run(r.connect(hostname, port))
		self.conn = r.connect(hostname, port)
		self.dbRef = r.db(self.dbName)

	def initPipelineTables(self): 

		spotData = {
		"trade_id": self.NONE,
		"price": self.NONE,
		"size": self.NONE,
		"bid": self.NONE,
		"ask": self.NONE,
		"volume": self.NONE,
		"time": self.NONE
		}

		techIndicators = dict.fromkeys(self.techInds)
		self.dbRef.table_create("SpotData").run(self.conn)
		self.dbRef.table("SpotData").insert(spotData).run(self.conn)
		self.dbRef.table_create("TechIndicators").run(self.conn)
		self.dbRef.table("TechIndicators").insert(techIndicators).run(self.conn)

	def initStatisticsTables(self): 

		riskData = {
		'KellyCriterion': self.NONE, 
		'SharpeRatio' : self.NONE, 
		'Alpha' : self.NONE,
		'Beta': self.NONE
		}

		capitalData = {
		'capital' : self.NONE, 
		"commission" : self.NONE, 
		"return" : self.NONE
		}

		self.dbRef.table_create("RiskData").run(self.conn)
		self.dbRef.table("RiskData").insert(riskData).run(self.conn)
		self.dbRef.table_create("CapitalData").run(self.conn)
		self.dbRef.table("CapitalData").insert(capitalData).run(self.conn)

	def initTradingTable(self): 
		self.dbRef.table_create("PositionCache").run(self.conn)

	def initBookTables(self): 
		self.dbRef.table_create("PositionBook").run(self.conn)

	def setTradingParams(self, exchange, ticker, techInds, tradeQuan=1, tolerance=.05):

		self.exchange, self.ticker, self.tradeQuantity = exchange, ticker, tradeQuan
		self.tolerance, self.techInds = tolerance, techInds

	def setHistoricalParams(self, histInterval, histLag):
		self.histInterval, self.histLag = histInterval, histLag

	def generateTechIndObjects(self, histDF):
		if (self.techInds != {}): 
			self.techInds = [Indicator(histDF,k,*v) for k,v in self.techInds.items()]

	def start(self, strat, capital, commission):

		self.initDatabase()
		self.initPipelineTables()
		self.initStatisticsTables()
		self.initTradingTable()
		self.initBookTables()

		entryConditions, exitConditions = stratFuncs
		strat = stra.Strategy(stratName, entryConditions, exitConditions)
		self.databaseManager = dbm.DatabaseManager(self.dbRef, self.conn, strat, auth)
		self.databaseManager.setTradingParameters(self.exchange, self.ticker)

	def run(self, typeCode, endTime): 

		plInstance, histData = plu.Pipeline(histInterval), None
		endTimeUNIX = utl.dateToUNIX(endTime)
		startDate = utl.getCurrentDateStr()
		priorDate = utl.datetimeDiff(startDate, 30)
		marketData = (self.ticker, self.tradeQuantity)
		systemData = (endTimeUNIX, histLag, systemLag, plInstance)

		if (self.ticker in cst.GDAX_TICKERS):
			gdaxTicker = cst.GDAX_TO_POLONIEX[self.ticker]
			histData = plInstance.getCryptoHistoricalData(gdaxTicker, priorDate, startDate)	
		else:
			raise ValueError('Bad ticker! Supported tickers are BTC, LTC, ETH.')

		self.generateTechIndObjects(histData)
		sysTuple = (marketData, systemData)

		if (typeCode == "BT"):
			from Pipeline import indsToDF
			techDF = indsToDF(self.techInds)
			positionData = ()
			return self.loopBacktestLogic(positionData, histData, techDF) 

		if (typeCode == "PT"):
			self.loopPaperTradeLogic(*sysTuple, histData)
			return self.endPaperTrading(endCode, sysTuple)

	def loopBacktestLogic(self, positionData, histDF, techDF):

		capital, commission, quantity, tolerance, posTotal = positionData
		strategy, trading, books = 'strategy', 'trading', 'books'

		for row in zip(histDF.itertuples(), techDF.itertuples()):

			self.databaseManager.read(strategy, "tryEntryStrategy", stratData)
			self.databaseManager.read(strategy, "tryExitStrategy", stratData)
			entryVerdict, exitVerdict = self.databaseManager.processTasks()

			self.databaseManager.read(trading, 'verifyAndEnterPosition', entryVerdict, *positionData)
			entryPos, capitalRemaining = self.databaseManager.processTasks()
			capital = capitalRemaining
			
			self.databaseManager.write(books, 'addToPositionCache', entryPos)
			self.databaseManager.read(trading, 'exitValidPositions', exitVerdict)
			completedPositions, capitalGained = self.databaseManager.processTasks()
			capital += capitalGained

			self.databaseManager.write(books, 'addToPositionBook', completedPositions)
			self.databaseManager.processTasks()

		positionBook = self.databaseManager.collectBacktestData()
		return (capital, positionBook)

	def loopPaperTradeLogic(self):

		endTimeUNIX, histLag, systemLag, plInstance = systemData

		while (endTimeUNIX > utl.getCurrentTimeUNIX()): 

			self.databaseManager.write("statistics", "updateCapitalStatistics")
			self.databaseManager.write("pipeline", "updateSpotData", self.ticker)
			self.databaseManager.read("statistics", "pullCapitalStatistics")
			capitalStats = self.databaseManager.processTasks()

			self.databaseManager.write("pipeline", "updateTechIndicators", self.ticker, self.techInds, indLag)
			self.databaseManager.read("pipeline", "pullPipelineData")
			stratData = self.databaseManager.processTasks()

			self.databaseManager.read("strategy", "tryEntryStrategy", stratData)
			self.databaseManager.read("strategy", "tryExitStrategy", stratData)
			entryVerdict, exitVerdict = self.databaseManager.processTasks()

			self.databaseManager.read('trading', 'verifyAndEnterPosition', entryVerdict, capitalStats, orderData)
			filledOrder, entryPos = self.databaseManager.processTasks()
			
			self.databaseManager.write('trading', 'addToPositionCache', entryPos)
			self.databaseManager.write("statistics", "updateCapitalStatistics")
			self.databaseManager.read('trading', 'exitValidPositions', exitVerdict, marketData)
			filledExitOrders, completedPositions = self.databaseManager.processTasks()

			self.databaseManager.write('books', 'addToPositionBook', completedPositions)
			self.databaseManager.processTasks(), time.sleep(systemLag)

	def endPaperTrading(self, endCode, sysTuple): 

		"""logic to close all remaining positions in cache, add to oBook, pBook.
		endCode decides a hard exit or soft exit, e.g wait for strategies
		or close out of all positions regardless of strats
		"""

		if (endCode == cst.SOFT_EXIT): 

			print("SOFT_EXIT INITIATED. ALL ONGOING TRADES BEING FINALIZED.")
			tradingRef = self.dbRef.table("PositionCache")
			while (int(self.tradingRef.count().run(self.conn)) > 0):
				self.loopSystemLogic(*sysTuple)
		
		if (endCode == cst.HARD_EXIT):

			print("HARD_EXIT INITIATED. ALL ONGOING TRADES TERMINATED.")
			self.databaseManager.read('trading', 'exitValidPositions', cst.HARD_EXIT, marketData)
			filledExitOrders, completedPositions = self.databaseManager.processTasks()
			
			self.databaseManager.write("statistics", "updateCapitalStats")
			self.databaseManager.write('books', 'addToPositionBook', completedPositions)
			self.databaseManager.write('books', 'addToOrderBook', filledExitOrders)
			self.databaseManager.processTasks()
		
		rStats, cStats, oBook, pBook = self.databaseManager.collectInstData()
		r.db_drop(self.dbName).run(self.conn)
		histDF = self.techInds[0].getDataframe()
		return (rStats, cStats, oBook, pBook, histDF)
