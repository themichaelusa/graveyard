
def scrapeSP500():
	import requests
	from bs4 import BeautifulSoup

	data = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text
	html = BeautifulSoup(data, 'lxml')
	companiesTable = html.find('div', class_='mw-parser-output').find('table')
	allCompanies = companiesTable.find_all('tr')[2:]

	completeList = []
	for company in allCompanies: 
		filings = company.find_all('a', class_="external text")[1]['href']
		companyData = company.text.split('\n')
		companyData = [data for data in companyData if data != '']
		ticker, fullName = companyData[0:2]
		giscSector, giscSubIndustry = companyData[3:5]
		CIK = companyData[len(companyData)-1]
		completeList.append((ticker, fullName, CIK, filings, giscSector, giscSubIndustry))

	return completeList
