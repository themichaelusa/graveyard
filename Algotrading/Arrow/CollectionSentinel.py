import ArrowSentinel

#class CollectionSentinel(ArrowSentinel):
class CollectionSentinel(object):
	def __init__(self, funcs):
		#super().__init__(funcs)
		self.names = list(funcs.keys())
		self.funcs = funcs

	def generatePipelessTasks(self):
		import asyncio

		pipelessTasks = []
		for k,v in self.funcs.items():
			if (v[1] is None):
				asyncFunc = v[0] 
				future = asyncio.ensure_future(asyncFunc())
				pipelessTasks.append((k, future))
				if (self.names == []):
					break
				else:
					self.names.remove(k)

		taskNames, taskFutures = zip(*pipelessTasks)
		return taskNames, asyncio.gather(*taskFutures)

	"""
	def generatePipedTasks(self, piper):
		import asyncio

		pipedTasks = []
		for k,v in self.funcs.items():
			if (v[1] is not None and v[1] == piper):
				asyncFunc = v[0] 
				future = asyncio.ensure_future(asyncFunc())
				pipedTasks.append(((k, v[2]), future))
				if (self.names == []):
					break
				else:
					self.names.remove(k)

		taskData, taskFutures = zip(*pipedTasks)
		return taskData, asyncio.gather(*taskFutures)

	def generateAllCollectionTasks(self):
		pipeless = self.generatePipelessTasks()
		piped = [self.generatePipedTasks(p) for p in pipeless[0]]
		
		#print(self.names)
		#while self.names != []:
		for func in self.names:
			if (self.names == []):
				break
			else:
				continue


		#print(pipeless, piped)
	"""





