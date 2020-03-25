import constants as cons
import utilities as ut
import json, requests
import pandas as pd
import numpy as np

class Pipeline(object):

    def __init__(self, url, urlArgs):

        self.url = url
        self.urlArgs = urlArgs

    class Formatter(object):

        def __init__(self, json):
            self.json = json
            self.dataframe = cons.NOT_SET
            self.nparray = cons.NOT_SET

        def toDataframe(self):

            self.dataframe = pd.DataFrame.from_records(self.json)
            return self.dataframe

        def toNumpyArray(self):

            self.nparray = np.array(list(self.json.values()))
            return self.nparray

        def toDictionary(self):

            df = self.dataframe

            talibInputs = {
            'open': np.asarray(df["open"].tolist()),
            'high': np.asarray(df["high"].tolist()),
            'low': np.asarray(df["low"].tolist()),
            'close': np.asarray(df["close"].tolist()),
            'volume': np.asarray(df["volume"].tolist())
            }

            return talibInputs

    def RESTConnect(self, formattedArgs): return requests.get(self.url + formattedArgs).json()

    def getHistoricalData(self, currency, period, startDate, endDate):

        formattedStartDate = ut.dateToUNIX(startDate)
        formattedEndDate = ut.dateToUNIX(endDate)

        formmatedURLArgs = self.urlArgs.format(str(currency), str(formattedStartDate), str(formattedEndDate), str(period))
        histJSON = self.RESTConnect(formmatedURLArgs)
        dataToReturn = Pipeline.Formatter(histJSON)

        return (dataToReturn.toDataframe(), dataToReturn.toDictionary())

    def packageHistoricalData(self, histData, laggedHistData):

        histData = histData[0]
        BBANDS_Data = ut.BOL_BANDS(cons.OPTIMAL_BBANDS_MA, 2, 2, 2, laggedHistData[1])
        MA_Data = ut.MOV_A(cons.OPTIMAL_MA, 2, laggedHistData[1]) 
        RSI_Data = ut.RSI_IND(2, laggedHistData[1])

        formattedData = []
        formattedMA = ut.extendList(MA_Data)
        formattedRSI = ut.extendList(RSI_Data)
        formattedUBBANDS = ut.extendList(BBANDS_Data[0])
        formattedLBBANDS = ut.extendList(BBANDS_Data[2])

        for i in range(len(histData['close'])):
            formattedDate = ut.UNIXtoDate(histData['date'][i])
            formattedData.append((formattedDate, histData['close'][i], formattedMA[i], formattedRSI[i], formattedUBBANDS[i], formattedLBBANDS[i], histData['volume'][i]))

        df = pd.DataFrame.from_records(formattedData, columns = ['Date', 'Close', 'MA', 'RSI', 'Upperband', 'Lowerband', 'Volume'])
        df = df.set_index(pd.DatetimeIndex(df['Date']))
        histDatesToReturn = df.index.to_pydatetime()
        df = df.drop(['Date'], axis=1)

        return (df, ut.date2numWrapper(histDatesToReturn))

    def getLiveData(self, currency):

        formmatedURLArgs = self.urlArgs.format(str(currency))
        histJSON = self.RESTConnect(formmatedURLArgs)
        dataToReturn = Pipeline.Formatter(histJSON)

        return dataToReturn.toNumpyArray()

# TODO: Inclusion of gain, commission functions to more accurately report Profit (not assigned yet)

"""
This method takes in the finished algorithm data, in the form of Position objects, and in two flavors (Buy and Sell).
GAIN_PER_CENT is passed in for roughly calculating the profit you make per position per cent of the currency
appreciating or depreciating.
"""

def algoResultsToDataframe(buyPositions, sellPositions, GAIN_PER_CENT):

    toDataframe = []

    for i in range(len(buyPositions)):

        curPos = buyPositions[i]
        if (curPos == None): continue

        currPosDiff = curPos.entryPrice - curPos.exitPrice
        moneyMade = (100 * currPosDiff) * GAIN_PER_CENT
        # moneyMade -= moneyMade*.004
        
        if (currPosDiff > 0 == False): # winning pos
            toDataframe.append((curPos.entryDatetime, curPos.longshort, curPos.entryPrice, curPos.exitPrice, -moneyMade, curPos.exitDatetime))
        else: toDataframe.append((curPos.entryDatetime, curPos.longshort, curPos.entryPrice, curPos.exitPrice, -moneyMade, curPos.exitDatetime))
    
    for i in range(len(sellPositions)):

        curPos = sellPositions[i]
        if (curPos == None): continue

        currPosDiff = curPos.entryPrice - curPos.exitPrice
        moneyMade = (100 * currPosDiff) * GAIN_PER_CENT
       # moneyMade -= moneyMade*.004

        if (currPosDiff > 0 == True): # winning pos
            toDataframe.append((curPos.entryDatetime, curPos.longshort, curPos.entryPrice, curPos.exitPrice, moneyMade, curPos.exitDatetime))
        else: toDataframe.append((curPos.entryDatetime, curPos.longshort, curPos.entryPrice, curPos.exitPrice, moneyMade, curPos.exitDatetime))
    

    dataframe = pd.DataFrame.from_records(toDataframe, columns = ['EntryTime', 'Position', 'EntryPrice', 'ExitPrice', 'Profit' ,'ExitTime'])
    allEntryTimes = dataframe['EntryTime']

    dataframe = dataframe.set_index(pd.DatetimeIndex(allEntryTimes))
    dataframe = dataframe.drop(['EntryTime'], axis=1)

    return (dataframe, allEntryTimes)

