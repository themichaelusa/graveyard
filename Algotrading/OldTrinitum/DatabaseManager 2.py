import asyncio
import rethinkdb as r
import Constants as cst
import AsyncManager as asm
from poloniex import Poloniex
from AsyncPQ import AsyncReadWriteQueue

class DatabaseManager(object):

	def __init__(self, dbReference, conn, strat, auth):
		
		self.strat = strat
		self.connObj = conn
		self.dbReference = dbReference

		self.classDict = {
		'pipeline': asm.AsyncPipelineManager(dbReference, conn),
		'strategy': asm.AsyncStrategyManager(dbReference, conn, strat),
		'statistics': asm.AsyncStatisticsManager(dbReference, conn, auth),
		'trading': asm.AsyncTradingManager(dbReference, conn, auth),
		'books': asm.AsyncBookManager(dbReference, conn)
		}
		self.rwQueue = AsyncReadWriteQueue(self.classDict)

	def setTradingParameters(self, quantity, ):

		self.classDict['trading'].quantity = quantity
		self.classDict['trading'].symbol = symbol

	def read(self, tableName, operation, *opargs): 
		self.rwQueue.cdRead(tableName, operation, *opargs)

	def write(self, tableName, operation, *opargs): 
		self.rwQueue.cdWrite(tableName, operation, *opargs)

	def processTasks(self):
		return self.rwQueue.processTasks() 

	def collectBacktestData(self):
		self.read('books', "getPositionBook")
		return self.processTasks()

	def collectPaperTradeData(self):

		statistics, books = "statistics", "books"
		self.processTasks() # finish any remaining tasks
		self.read(statistics, "pullRiskStats")
		self.read(statistics, "pullCapitalStats")
		self.read(books, "getPositionBook")
		return self.processTasks()
