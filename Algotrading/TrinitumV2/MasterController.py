class MasterController(object):

	def __init__(self, instanceController):
		self.instanceController = instanceController
		self.RequestEngine = RequestEngine()

	def routePipelineData(self):

	def updateMasterDB(self):
		
class RequestEngine(object):

	def __init__(self):
		self.activeInstances = {}
		self.requestQueue = []

	def get(self): pass

	def push(self): pass 

	def refreshInstances(self):
		active = self.instanceController.getActiveInstances()
		activeDict = {k:v for v.instanceName, v in active}
		self.activeInstances = activeDict

		