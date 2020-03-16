import pandas as pd
import utilities as ut
import algorithm as alg
import constants as cons
from matplotlib import pyplot as plt

# TODO: Refactor UI Method to allow Python3 shell commands for easier backtests (Michael)

def CMD_UI(displayUIInfo, ticker, dateToday):

    predictionAccuracy, errorTotal, profitTotal, buyAccuracy, sellAccuracy = displayUIInfo[0]
    totalPositionsLen, validPositionsLen, neutralPositionsLen, invalidPositionsLen = displayUIInfo[1]

    print("\n" + "ALGORITHM V1.2 RESULTS FOR " + ticker + " on: " + str(dateToday) + "\n")
    print("# of Valid Positions(gain): " + str(validPositionsLen))
    print("# of Neutral Positions(loss on commission): " + str(neutralPositionsLen))
    print("# of Invalid Positions(loss): " + str(invalidPositionsLen) + "\n")

    print("Total Accuracy: " + str(predictionAccuracy) + "%")
    print("Total Error: " + str(errorTotal) + "%" + "\n")

    print("Buy Accuracy: " + str(buyAccuracy) + "%")
    print("Sell Accuracy: " + str(sellAccuracy) + "%")

    print("Returns: " + "$" + str(profitTotal))
    print("Profit: " + str((profitTotal/2000) * 100) + "%" + "\n")



def verifyBacktestAccuracy(algoDF, additionalDiagnostics):

    validBuyPositions, validSellPositions = [],[]
    invalidBuyPositions, invalidSellPositions = [],[]
    equalBuyPositions, equalSellPositions = [],[]

    allPositions = algoDF[0]['Position']
    allEntryPrices = algoDF[0]['EntryPrice']
    allExitPrices = algoDF[0]['ExitPrice']
    allEntryTimes = algoDF[1]

    for i in range(len(allPositions)):

        if(allPositions[i] == cons.BUY):

            if(allEntryPrices[i] < allExitPrices[i]): validBuyPositions.append(allPositions[i])
            if(allEntryPrices[i] > allExitPrices[i]): invalidBuyPositions.append(allPositions[i])
            if(allEntryPrices[i] == allExitPrices[i]): equalBuyPositions.append(allPositions[i])

        if(allPositions[i] == cons.SELL):

            if(allEntryPrices[i] > allExitPrices[i]): validSellPositions.append(allPositions[i])
            if(allEntryPrices[i] < allExitPrices[i]): invalidSellPositions.append(allPositions[i])
            if(allEntryPrices[i] == allExitPrices[i]): equalSellPositions.append(allPositions[i])

    totalPositionsLen = len(allPositions)
    validPositionsLen = len(validBuyPositions) + len(validSellPositions)
    neutralPositionsLen = len(equalBuyPositions) + len(equalSellPositions)
    invalidPositionsLen = len(invalidBuyPositions) + len(invalidSellPositions)

    allBuyPosLen = len(validBuyPositions) + len(equalBuyPositions) + len(invalidBuyPositions)
    allSellPosLen = len(validSellPositions) + len(equalSellPositions) + len(invalidSellPositions)

    predictionAccuracy = (100*((validPositionsLen + neutralPositionsLen)/totalPositionsLen))
    buyAccuracy = (100*((len(validBuyPositions) + len(equalBuyPositions))/allBuyPosLen))
    sellAccuracy = (100*((len(validSellPositions) + len(equalSellPositions))/allSellPosLen))

    errorTotal = (100*(invalidPositionsLen/totalPositionsLen))
    profitTotal = algoDF[0]['Profit'].sum(axis=0)

    displayUIInfo = (predictionAccuracy, errorTotal, profitTotal, buyAccuracy, sellAccuracy)
    AllPositionsLen = (totalPositionsLen, validPositionsLen, neutralPositionsLen, invalidPositionsLen)

    if (additionalDiagnostics == True):

        buyPosToReturn = (validBuyPositions, equalBuyPositions, invalidBuyPositions)
        sellPosToReturn = (validSellPositions, equalSellPositions, invalidSellPositions)
        return (displayUIInfo, AllPositionsLen, buyPosToReturn, sellPosToReturn)

    return (displayUIInfo, AllPositionsLen)


# TODO: Start developing full diagnostic panel like: https://pmorissette.github.io/bt/index.html (Not assigned yet) 

def extendedDiagnostics(): 
    temp = cons.NOT_SET


# TODO: Method to export everything in one go (CSV's, Plots, Full Panel, Accuracy Report, etc) to separate folder in directory (Not assigned yet) 

def exportDiagnosticsPanel(): 
    print(extendedDiagnostics())


# TODO: Figure out plotting buy/sell signals with matplotlib && research other necessary data to plot (Not assigned yet) 

def testPlot(meanReversionDataframe):
    temp = cons.NOT_SET
    """
    currentDF = meanReversionDataframe[0]
    currentPrice = currentDF['Close'][len(['Close'])]
    buySignals, sellSignals, signalDT = applyTradingLogic(meanReversionDataframe)

    currentDF.Upperband.plot(label='UpperBBAND')
    currentDF.Lowerband.plot(label='LowerBBAND')
    currentDF.Close.plot(label='Price')
    plt.plot(signalDT, currentDF.Close, '-g^', markevery = buySignals)
    plt.plot(signalDT, currentDF.Close, '-rv', markevery = sellSignals)

    # plt.plot(buySignals[0], buySignals[1],'g^')
    # plt.plot(sellSignals[0], sellSignals[1],'r^')

    # plt.ylim(-1.5 * currentPrice, 1.5 * currentPrice)
    plt.legend(bbox_to_anchor=(1.25, .5))
    plt.tight_layout()
    # plt.show()
    """
