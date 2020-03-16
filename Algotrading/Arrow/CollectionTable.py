class CollectionTable(object):
	
	def __init__(self, inputs, pipes):
		self.inputs = inputs
		self.pipes = pipes
		self.funcs = self.generateFuncs()

	def generateAsyncFunction(self, input, sleep=0):
		
		async def genericAsync():
			output, exception = None, None
			try:
			 	output = input.funcRef(*input.funcArgs)
			except Exception as e:
			 	exception = e 
			await asyncio.sleep(sleep)

			if (type(output) == input.outType):
				return (output, exception, True)
			else:
				return (output, exception, False)

		return genericAsync

	def generateAsyncFuncs(self): 
		return {name: self.generateAsyncFunction(func) for name,func in self.inputs.items()}

	def generateFuncs(self):
		asyncFuncs = self.generateAsyncFuncs()
		funcs = {}

		for k,v in asyncFuncs.items():
			if k in self.pipes:
				piperName, byElem = self.pipes[k]
				funcs.update({k: (v, piperName, byElem)})
			else:
				funcs.update({k: (v, None, None)})

		return funcs


		