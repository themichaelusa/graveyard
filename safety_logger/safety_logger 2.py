
class Logger(object):
	
	def __init__(self, ):	
		self.CacheUnits = []

	class CacheUnit(object):

		def __init__(self, funcRef, funcArgs, returnType, errorCode):
			
			self.funcRef, self.funcArgs = funcRef, funcArgs
			self.returnValue, self.returnType = None, returnType
			self.functionName = funcRef.__name__
			self.errorCode = errorCode

		def computeFunction(self):

			try:

				self.returnValue = self.funcRef(*self.funcArgs)
				computedReturnType = type(self.returnValue)
				typeErrorRef = self.errorCode[1]

				if (computedReturnType == self.returnType):
					typeErrorRef = "CORRECT_TYPE"
				else: 
					typeErrorRef = "BAD_TYPE" + str(computedReturnType)

			except Exception as e:
				self.errorCode[2] = e

			finally:
				return {self.functionName: (self.returnValue, *self.errorCode)}

		def resetUnit(self):
			if (self.returnValue is None): pass
			else: self.returnValue = None

	def addLoggingUnit(self, funcRef, fArgs, returnType, errorCode):



	def generateOutputDict(self):
		return 
					