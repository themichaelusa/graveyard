import time
import asyncio
import Order as order
import Position as pos
import rethinkdb as r
import Constants as cst
import Utilities as utl
import Pipeline as plu

import gdax
import uuid

class AsyncTaskManager(object):

	def __init__(self, dbReference, connection): 
		
		self.funcDict = {}
		self.connection = connection
		self.dbReference = dbReference

	def setFunctionDict(self, newDict):
		self.funcDict = newDict

	def pullTableContents(self, tableRef):

		contents = tableRef.run(self.connection)
		return [data for data in contents]

class AsyncPipelineManager(AsyncTaskManager):

	def __init__(self, dbReference, connection): 		

		super().__init__(dbReference, connection)
		self.formatterInstance = plu.Formatter()
		self.gdaxPublicClient = gdax.PublicClient()
		self.spotDataRef = self.dbReference.table('SpotData')
		self.techIndsRef = self.dbReference.table('TechIndicators')
		self.spotPrice, self.spotVolume = (None,)*2

	async def updateSpotData(self, symbol): #write

		spotData = dict(self.gdaxPublicClient.get_product_ticker(symbol))
		self.spotPrice, self.spotVolume = float(spotData['price']), float(spotData['volume'])
		self.spotDataRef.update(spotData).run(self.connection)
		await asyncio.sleep(0)

	async def updateTechIndicators(self, symbol, techIndsList, lag = 1): #write

		OHLCV = list(self.gdaxPublicClient.get_product_24hr_stats(symbol).values())[:3]
		OHLCV = [float(data) for data in OHLCV]
		OHLCV.extend([self.spotPrice, self.spotVolume])

		techIndDict = {}
		for ind in techIndsList:
			techIndDict.update({ind.tbWrapper.indicator: ind.getRealtime(OHLCV, lag)})
		
		self.techIndsRef.update(techIndDict).run(self.connection)
		await asyncio.sleep(0)

	async def pullPipelineData(self): #read

		sdData = self.pullTableContents(self.spotDataRef)
		tiData = self.pullTableContents(self.techIndsRef)

		formattedSDData = self.formatterInstance.formatSpotData(sdData[0])
		formattedTIData = self.formatterInstance.formatTechIndicators(tiData[0])
		formattedTickData = tuple(formattedSDData + formattedTIData)
		
		await asyncio.sleep(.5)
		return formattedTickData

class AsyncStrategyManager(AsyncTaskManager):
	
	def __init__(self, dbReference, connection, strat): 		
		
		super().__init__(dbReference, connection)
		self.strategy = strat
		self.tradingRef = self.dbReference.table('PositionCache')

	async def tryEntryStrategy(self, tickData): #read

		entryResult = self.strategy.tryEntryStrategy(tickData)
		if (entryResult == 1): print("ENTRY CONDS VALID")
		await asyncio.sleep(0)
		return entryResult

	async def tryExitStrategy(self, tickData): #read

		pCacheSize = int(self.tradingRef.count().run(self.connection))
		exitResult = self.strategy.tryExitStrategy(pCacheSize, tickData)
		if (exitResult == 1): print("EXIT CONDS VALID")
		await asyncio.sleep(0)
		return exitResult

class AsyncStatisticsManager(AsyncTaskManager):

	def __init__(self, dbReference, connection, authData): 		
		
		super().__init__(dbReference, connection)
		self.gdaxAuthClient = gdax.AuthenticatedClient(*authData)
		self.RiskStatsRef = self.dbReference.table('RiskData')
		self.CapitalStatsRef = self.dbReference.table('CapitalData')

	async def updateRiskStatistics(self, rsuDict):
		
		self.RiskStatsRef.update(rsuDict).run(self.connection)
		await asyncio.sleep(0)

	async def updateCapitalStatistics(self, capital):

		accountData = list(self.gdaxAuthClient.get_accounts())
		acctDataUSD = list(filter(lambda x: x['currency'] == "USD", accountData))
		availibleCapitalUSD = float(acctDataUSD[0]['available'])

		capitalDict = {
		'capital': availibleCapitalUSD, 
		"commission": 'None', 
		"return": 'None'
		}

		self.CapitalStatsRef.update(capitalDict).run(self.connection)
		await asyncio.sleep(0)

	async def pullRiskStatistics(self): 

		RiskStats = self.pullTableContents(self.RiskStatsRef)
		await asyncio.sleep(.5)
		return RiskStats[0]

	async def pullCapitalStatistics(self): 

		CapitalStats = self.pullTableContents(self.CapitalStatsRef)
		await asyncio.sleep(.5)
		return CapitalStats[0]
	
class AsyncTradingManager(AsyncTaskManager):

	def __init__(self, dbReference, connection, authData): 		

		super().__init__(dbReference, connection)
		self.pCacheRef = self.dbReference.table('PositionCache')
		self.RiskStatsRef = self.dbReference.table('RiskStats')
		self.CapitalStatsRef = self.dbReference.table('CapitalStats')		
		self.exchange = cst.NOT_SET
		self.symbol = cst.NOT_SET

	async def verifyAndEnterPosition(self, entryCond, capitalStats, marketData): #read

		newPosition, currentCapital = None, capitalStats['capital']
		validEntryConditions = entryCond == 1 and currentCapital > 0
		
		if (validEntryConditions): 

			spotPrice, tolerance, direction, ticker, quantity = marketData
			fundToleranceAvailible = currentCapital*tolerance > quantity*spotPrice
			#check db for viable kelly criterion values, max draw, etc. (not done)
			
			if (fundToleranceAvailible):

				orderFillTime = orderStatus['done_at']
				orderData = (direction, ticker, size, float(response['executed_value']), orderFillTime)
				newPosition = pos.Position(uuid.uuid4(), *orderData)
			
		await asyncio.sleep(.5)
		return newPosition

	async def exitValidPositions(self, exitVerdict, marketData): #read

		positionCache = self.pullTableContents(self.pCacheRef)
		completedPositions, exitOrders = [None], [None]

		if (exitVerdict != 0 and positionCache != []):

			sellResponses, completedPositions, exitOrders = [], [], []
			ticker, size = marketData

			for p in positionCache:

				response = dict(self.gdaxAuthClient.sell(product_id=ticker, type='market', funds=size))
				pArgs = (p['entID'], p['direction'], p['ticker'], p['quantity'], p['entryPrice'], p['entryTime'])
				completedPosition = pos.Position(*pArgs)
				completedPosition.setExitID(response['id'])
				completedPositions.append(completedPosition)
				sellResponses.append(response)

				exitOrder = order.Order('EX', 'S', ticker, size)
				exitOrder.setErrorCode("NO_ERRORS")
				exitOrder.setOrderID(response['id'])
				exitOrders.append(exitOrder)

			time.sleep(1)

			for posit, response in zip(completedPositions, sellResponses):
				
				posEXID = posit.exID
				orderStatus = dict(self.gdaxAuthClient.get_order(posEXID))
				orderExitTime = orderStatus['done_at']
				posit.setExitParams(float(response['executed_value']), orderExitTime)
				print("Exited Position:", posEXID, "at time:", orderExitTime)

			self.pCacheRef.delete().run(self.connection)			
		
		await asyncio.sleep(.5)
		return (exitOrders, completedPositions)

	async def addToPositionCache(self, position): #write

		if (position is not None):
			pDict = utl.getObjectDict(position)
			self.pCacheRef.insert(pDict).run(self.connection)
		
		await asyncio.sleep(0)

class AsyncBookManager(AsyncTaskManager):
	
	def __init__(self, dbReference, connection):

		super().__init__(dbReference, connection)
		self.orderBookRef = self.dbReference.table('OrderBook')
		self.posBookRef = self.dbReference.table("PositionBook")

	async def addToPositionBook(self, positions): #write

		if (positions != [None]):
			for position in positions:
				pDict = utl.getObjectDict(position)
				self.posBookRef.insert(pDict).run(self.connection)
			
		await asyncio.sleep(0)

	async def getPositionBook(self): #read
	
		PositionBook = self.pullTableContents(self.posBookRef)
		await asyncio.sleep(.5)
		return PositionBook
