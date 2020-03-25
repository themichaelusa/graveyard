class TradingInstance(object):
	
	def __init__(self, name, exchange, symbol):
		self.name, self.exchange, self.symbol = name, exchange, symbol
		self.active = True

		from .Constants import DEFAULT_QUANTITY, DEFAULT_RISK_TOL, DEFAULT_POS_LIMIT
		from .Constants import DEFAULT_IND_LAG, DEFAULT_SYS_LAG 
		self.quantity = DEFAULT_QUANTITY
		self.tolerance = DEFAULT_RISK_TOL
		self.poslimit = DEFAULT_POS_LIMIT
		self.indicatorLag = DEFAULT_IND_LAG
		self.systemLag = DEFAULT_SYS_LAG 
		self.techInds = {}

	def isActive(self): 
		return self.active

	def getPendingRequests(self): pass

	def setTradingParams(self, techInds, tolerance, poslimit, quantity):
		self.techInds, self.tolerance, self.poslimit, self.quantity = techInds, tolerance, poslimit, quantity

	def generateIndicators(self, indicators):
		if (indicators != {}): 
			from realtime_talib import Indicator
			self.techInds = [Indicator(histDF,k,*v) for k,v in self.techInds.items()]
		
	def setLagParams(self, indicatorLag, systemLag):
		self.indicatorLag, self.systemLag = indicatorLag, systemLag

	def runSystemLogic(self):

		try:
			self.databaseManager.write("pipeline", "updateSpotData")
			self.databaseManager.write("statistics", "updateCapitalStatistics")
			self.databaseManager.read("statistics", "pullCapitalStatistics")
			capitalStats = self.databaseManager.processTasks()

			self.databaseManager.write("pipeline", "updateTechIndicators", self.techInds, self.indicatorLag)
			self.databaseManager.read("pipeline", "pullPipelineData")
			stratData = self.databaseManager.processTasks()
			spotPrice = stratData['price']

			self.databaseManager.read("strategy", "tryStrategy", stratData)
			stratVerdict = self.databaseManager.processTasks()

			self.databaseManager.read('trading', 'createOrders', stratVerdict)
			entryOrder = self.databaseManager.processTasks()
			potentialEntryOrder = bool(entryOrder != None)

			self.databaseManager.write("statistics", "updateCapitalStatistics", potentialEntryOrder)
			self.databaseManager.read('trading', 'verifyAndEnterPosition', entryOrder, capitalStats, spotPrice)
			filledOrder, entryPos = self.databaseManager.processTasks()
			potentialPositionEntry = bool(filledOrder != [None])
			
			self.databaseManager.write('trading', 'addToPositionCache', entryPos)
			self.databaseManager.write('books', 'addToOrderBook', filledOrder)
			self.databaseManager.write("statistics", "updateCapitalStatistics", potentialPositionEntry)
			self.databaseManager.read('trading', 'exitValidPositions', stratVerdict)
			filledExitOrders, completedPositions = self.databaseManager.processTasks()
			potentialExitMade = bool(potentialPositionEntry or filledExitOrders != [None])

			self.databaseManager.write("statistics", "updateCapitalStatistics", potentialExitMade)
			self.databaseManager.write('books', 'addToPositionBook', completedPositions)
			self.databaseManager.write('books', 'addToOrderBook', filledExitOrders)
			self.databaseManager.processTasks(), time.sleep(self.systemLag)
  			
		except BaseException as e:
			from .Utilities import getStackTrace
			stackTrace = getStackTrace(e)
			self.logger.addEvent('system', ('SYS_LOGIC_CRASH: ' + str(e)))
			self.logger.addEvent('system', ('SYS_LOGIC_CRASH_STACKTRACE: ' + str(stackTrace)))

		
class TradingInstance(object):
	
	def __init__(self, name):

		self.name, self.NONE = name, "None"
		self.auth, self.exchange, self.symbol = (None,)*3

		from .Constants import DEFAULT_QUANTITY, DEFAULT_RISK_TOL, DEFAULT_POS_LIMIT
		from .Constants import DEFAULT_IND_LAG, DEFAULT_SYS_LAG 
		self.quantity = DEFAULT_QUANTITY
		self.tolerance = DEFAULT_RISK_TOL
		self.poslimit = DEFAULT_POS_LIMIT
		self.indicatorLag = DEFAULT_IND_LAG
		self.systemLag = DEFAULT_SYS_LAG 
		self.techInds = None

		self.conn = None
		self.dbRef = None
		self.databaseManager = None
		self.logger = None

	"""
	The start function creates the RethinkDB instance 
	"""
	def start(self, stratName, stratFunc):
	
		self.initDatabase()
		self.initPipelineTables()
		self.initStatisticsTables()
		self.initTradingTable()
		self.initBookTables()

		from .Strategy import Strategy
		from .DatabaseManager import DatabaseManager
		strat = Strategy(stratName, stratFunc)
		self.databaseManager = DatabaseManager(self.dbRef, self.conn, strat, self.auth, self.logger)
		self.databaseManager.setTradingParameters(self.symbol, self.quantity, self.tolerance, self.poslimit)

	def run(self, endTime, histInterval, histPeriod, endCode): 

		from .Pipeline import Pipeline
		from .Constants import GDAX_TO_POLONIEX
		from .Utilities import dateToUNIX, getCurrentDateStr, datetimeDiff, getCurrentTimeUNIX

		plInstance, histData = Pipeline(histInterval), None
		endTimeUNIX = dateToUNIX(endTime)
		startDate = getCurrentDateStr()
		priorDate = datetimeDiff(startDate, histPeriod)

		gdaxTicker = GDAX_TO_POLONIEX[self.symbol]
		histData = plInstance.getCryptoHistoricalData(gdaxTicker, priorDate, startDate)	
		self.generateTechIndObjects(histData)
		sysStart = 'TRADING_INSTANCE ' + self.name + ' INIT'
		self.logger.addEvent('system', sysStart)

		try:
  			while (endTimeUNIX > getCurrentTimeUNIX()):
  				self.runSystemLogic()
		except BaseException as e:
			from .Utilities import getStackTrace
			stackTrace = getStackTrace(e)
			self.logger.addEvent('system', ('INSTANCE_CRASH: ' + str(e)))
			self.logger.addEvent('system', ('INSTANCE_CRASH_STACKTRACE: ' + str(stackTrace)))

		self.end(endCode)

	"""logic to close all remaining positions in cache, add to oBook, pBook.
	endCode decides a hard exit or soft exit, e.g wait for strategies
	or close out of all positions regardless of strats
	"""
	def end(self, endCode): 

		from .Constants import SOFT_EXIT, HARD_EXIT

		if (endCode == SOFT_EXIT): 
			try:
				self.logger.addEvent('system', "SOFT_EXIT INITIATED. ALL ONGOING TRADES BEING FINALIZED.")
				tradingRef = self.dbRef.table("PositionCache")
				while (int(tradingRef.count().run(self.conn)) > 0):
					self.runSystemLogic()
			except BaseException as e:
				from .Utilities import getStackTrace
				stackTrace = getStackTrace(e)
				self.logger.addEvent('system', ('SOFT_EXIT_FAILURE: ' + str(e)))
				self.logger.addEvent('system', ('SOFT_EXIT_FAILURE_STACKTRACE: ' + str(stackTrace)))

		if (endCode == HARD_EXIT):
			try:
				self.logger.addEvent('system', "HARD_EXIT INITIATED. ALL ONGOING TRADES TERMINATED.")
				self.databaseManager.read('trading', 'exitValidPositions', HARD_EXIT)
				filledExitOrders, completedPositions = self.databaseManager.processTasks()

				self.databaseManager.write("statistics", "updateCapitalStatistics")
				self.databaseManager.write('books', 'addToPositionBook', completedPositions)
				self.databaseManager.write('books', 'addToOrderBook', filledExitOrders)
				self.databaseManager.processTasks()
			except BaseException as e:
				from .Utilities import getStackTrace
				stackTrace = getStackTrace(e)
				self.logger.addEvent('system', ('HARD_EXIT_FAILURE: ' + str(e)))
				self.logger.addEvent('system', ('HARD_EXIT_FAILURE_STACKTRACE: ' + str(stackTrace)))

		rStats, cStats, oBook, pBook = self.databaseManager.collectInstData()
		sysEnd = 'TRADING_INSTANCE ' + self.name + ' END'
		self.logger.addEvent('system', sysEnd)
		r.db_drop(self.name).run(self.conn)

		# RDB directory removal too unintuitive for end user 
		#from .Utilities import removeRDB_Direc
		#removeRDB_Direc()

		from .Diagnostics import ResultFormatter
		results = ResultFormatter(self.name, self.logger.filename)
		results.getFormattedResults(rStats, cStats, oBook, pBook)