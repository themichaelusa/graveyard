def roundup(x):
	import math
	return int(math.ceil(x / 100.0)) * 100

def calculateEquityReturn(startAmt, avgReturn, divYield, yearlyAlloc, years):
	final, zccGain, rollover, totalShares = startAmt, 0, 0, 0
	#zccGain = roundup(startAmt/startIdxPrice)

	for i in range(years):
		final += (final*(avgReturn+divYield) + yearlyAlloc)
		#startIdxPrice *= (1+avgReturn)
		#final += roundup(final/)

	return final

def calculateBondGains(startAmt, bondYield, duration):
	final = startAmt
	for i in range(duration):
		final += (final*bondYield)
	return final

def compInterestFormula(startAmt, avgReturn, compTime, years):
	return startAmt*((1+ (avgReturn/compTime))**(years*compTime))

"""

capital = int(input("ENTER STARTING CAPITAL: $"))
years = int(input("ENTER INVESTMENT PERIOD (YEARS): "))
startEqCapital = capital*.85
startBondCapital = capital*.10

usReturn = int(calculateEquityReturn(startEqCapital*.75, .1, .05, 120000*.75, years))
print("USA EQUITY MARKET (S&P500) CAPITAL AFTER {} YEARS: $".format(years), usReturn)

internationalReturn = int(calculateEquityReturn(startEqCapital*.25, .0763, .0269, 120000*.25, years))
print("INTERNATIONAL EQUITY MARKET (VEU) CAPITAL AFTER {} YEARS: $".format(years), internationalReturn)

print("TOTAL EQUITY CAPITAL AFTER {} YEARS: $".format(years), internationalReturn+usReturn)
print("TOTAL BOND CAPITAL AFTER {} YEARS: $".format(years), calculateBondGains(startBondCapital, .017, years))

totalGains = internationalReturn+usReturn+startBondCapital
print("TOTAL PERSONAL CAPITAL AFTER {} YEARS: $".format(years), totalGains)

"""

capital = 1000000

usReturn1 = int(calculateEquityReturn(capital*.85*.75, .1, .05, 120000*.75, 5))
finalUS = int(calculateEquityReturn(usReturn1, .1, .05, 60000*.75, 5)) 
internationalReturn = int(calculateEquityReturn(capital*.85*.25, .0763, .0269, 120000*.25, 5)) 
finalInt = int(calculateEquityReturn(internationalReturn, .0763, .0269, 60000*.25, 5)) 
print("$", finalUS+finalInt)
