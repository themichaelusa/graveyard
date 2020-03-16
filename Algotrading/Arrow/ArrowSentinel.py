
def log(func):
	def getObjectDict(obj):
		fullObj = func(obj)
		return dict((key, getattr(fullObj, key)) for key in dir(fullObj) if key not in dir(fullObj.__class__))
	return getObjectDict

class ArrowSentinel(object):
	def __init__(self, funcs):
		self.funcs = funcs

	def execute(self): pass
