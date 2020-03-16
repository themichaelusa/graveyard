
class RiskFreeRate(object):

	def __init__(self):
		self.treasuryURL = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
		self.times = {
		"1mo": 1,
		"3mo": 2,
		"6mo": 3,
		"1yr": 4,
		"2yr": 5,
		"3yr": 6,
		"5yr": 7,
		"7yr": 8,
		"10yr": 9,
		"20yr": 10,
		"30yr": 11
		}

	def __call__(self, time):
		import requests
		from bs4 import BeautifulSoup

		data = requests.get(self.treasuryURL).text
		html = BeautifulSoup(data, 'lxml')

		targetYieldRow = html.find_all('tr', class_='evenrow')
		floatYield = targetYieldRow[len(targetYieldRow)-1]
		allYields = floatYield.find_all('td', class_='text_view_data')
		return float(allYields[self.times[time]].text)
