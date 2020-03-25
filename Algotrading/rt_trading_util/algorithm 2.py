import pipeline as pl
import utilities as ut
import constants as cons

class Position(object):
    def __init__(self, longshort, entryDatetime, entryPrice, exitDatetime, exitPrice):

        self.longshort = longshort
        self.entryDatetime = entryDatetime
        self.entryPrice = entryPrice
        self.exitDatetime = exitDatetime
        self.exitPrice = exitPrice


def trailingStopLossTrigger(orderType, inputList, currentIndex):

    previousIndex = inputList[currentIndex-1]

    if (orderType == cons.BUY):
        return ((previousIndex > inputList[currentIndex]))
    if (orderType == cons.SELL):
        return ((previousIndex < inputList[currentIndex]))


def simulatePosition(buysell, posEntryData, truncHistData):

    entryDT = ut.num2dateWrapper(posEntryData[0])
    remainingDatetime = truncHistData[2]
    closeData = truncHistData[0]

    for i in range(len(remainingDatetime)):

        currentClose = closeData[i]
        currentMA = truncHistData[1][i]
        currentStopUBand = truncHistData[3][i]
        currentStopLBand = truncHistData[4][i]
        currentDatetime = remainingDatetime[i]
        formattedDT = ut.num2dateWrapper(currentDatetime)
        
        if (buysell == cons.SELL_MARKER): # sell exit strategy
            
            sellExitPosition = Position(cons.SELL, entryDT, posEntryData[1], formattedDT, currentClose)
            trailingSL = trailingStopLossTrigger(cons.SELL, closeData, i)
            boolCloseLessMA = (currentClose <= currentMA)

            if ((currentClose >= (1.5 * posEntryData[1]))): 
                return sellExitPosition

            if (boolCloseLessMA and trailingSL == False): 
                continue
            elif (boolCloseLessMA and trailingSL == True): 
                return sellExitPosition

            if ((currentClose >= currentStopUBand)): 
                return sellExitPosition

        if (buysell == cons.BUY_MARKER): # buy exit strategy

            buyExitPosition = Position(cons.BUY, entryDT, posEntryData[1], formattedDT, currentClose)
            trailingSL = trailingStopLossTrigger(cons.BUY, closeData, i)
            boolCloseGreaterMA = (currentClose >= currentMA) 

            if ((currentClose <= (.5 * posEntryData[1]))): 
                return buyExitPosition

            if (boolCloseGreaterMA and trailingSL == False): 
                continue
            elif (boolCloseGreaterMA and trailingSL == True): 
                return buyExitPosition

            if ((currentClose <= currentStopLBand)): 
                return buyExitPosition


def tryAlgorithmLogic(histData):

    buyPositions, sellPositions = [],[]
    allClose = histData[0]['Close']
    allRSI = histData[0]['RSI']
    allMA = histData[0]['MA']
    allDatetime = histData[1]

    allUBand = histData[0]['Upperband']
    allSUBand = [i * cons.STOP_LOSS_UBAND for i in allUBand]

    allLBand = histData[0]['Lowerband']
    allSLBand = [i * cons.STOP_LOSS_LBAND for i in allLBand]

    for i in range(len(allDatetime)):

        if (allUBand[i] == allLBand[i] or (i == 0)): continue

        posEntryData = (allDatetime[i], allClose[i])
        truncHistData = (allClose[i:], allMA[i:], allDatetime[i:], allSUBand[i:], allSLBand[i:])

        if (allClose[i] >= (allUBand[i])): 
            sellPositions.append(simulatePosition(cons.SELL_MARKER, posEntryData, truncHistData))
        
        if (allClose[i] <= (allLBand[i])): 
            buyPositions.append(simulatePosition(cons.BUY_MARKER, posEntryData, truncHistData))

    return (buyPositions, sellPositions)
    