class MasterPipeline(object):

	def __init__(self, arg):
		self.arg = arg

	def generateTechIndObjects(self, indicators):
		if (indicators != {}): 
			from realtime_talib import Indicator
			self.techInds = [Indicator(histDF,k,*v) for k,v in self.techInds.items()]
		