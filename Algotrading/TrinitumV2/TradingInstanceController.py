class TradingInstanceController(object):

	def __init__(self):
		self.instances = {}
		
	def createNewInstance(self, instanceType, name): pass
		from .TradingInstance import TradingInstance
		self.instances.update({name: TradingInstance(name)})

	def startInstance(self, instanceName): pass
		self.instances[instanceName].run()

	def getActiveInstances(self): pass
		return list(filter(lamdba x: x == x.isActive(), self.instances))

	def removeInstance(self): pass
		inactive = list(filter(lamdba x: x == !x.isActive(), self.instances))

		for instance in inactive:
			self.instances.pop(instance.name)

	def collectInstanceRequests(self, instanceName):
		return self.instances[instanceName].getPendingRequests()
