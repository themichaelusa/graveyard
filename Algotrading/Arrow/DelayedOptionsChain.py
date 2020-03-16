
def marketwatchOptionChain(ticker):
	url = 'https://www.marketwatch.com/investing/stock/{}/options?countrycode=US&showAll=True'.format(ticker.lower())
	import requests
	from bs4 import BeautifulSoup

	data = requests.get(url).text
	html = BeautifulSoup(data, 'lxml')
	chain = html.find('table', class_='optiontable eightwide')

	calls, puts = [], []
	optiontable = chain.find_all('tr')
	headerExists, currentExpiry, colnHeaders = False, None, None

	for row in optiontable:
		cols = row.find_all('td')
		cols = [elem.text.strip() for elem in cols]
		excludeEmpty = [elem for elem in cols if elem] # Get rid of empty values

		if "Symbol" in excludeEmpty[0]:
			if (not headerExists):
				colnHeaders = [elem for elem in excludeEmpty if elem != "Symbol"]
				colnHeaders = colnHeaders[0:6]
				colnHeaders.insert(0, "Expiry")
				colnHeaders.insert(1, "Strike")
				headerExists = True

		if "Expires" in excludeEmpty[0]:
			currentExpiry = excludeEmpty[0][7:].strip()
		elif "quote" in excludeEmpty[0]:
			excludeQuote = [elem for elem in excludeEmpty if elem != "quote"]
			data = (currentExpiry, *excludeQuote)
			calls.append((data[0], data[7], *data[1:7]))
			puts.append((data[0], data[7], *data[8:]))

	import pandas as pd
	callsDF = pd.DataFrame(calls, columns=colnHeaders)
	putsDF = pd.DataFrame(puts, columns=colnHeaders)
	return callsDF, putsDF
