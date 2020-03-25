import ArrowSentinel 

"""
Collect Module:
Unify Separate Data Collection Scripts with 
central gatekeeper class that returns a 
CollectionTable. This class serves as a high level 
wrapper that communicates with the TaskScheduler and sends out
new jobs to be excecuted and returned. Cron jobs, type enforcement, 
and error handling done by the CollectionSentinel module.
"""

class Collect(object):

	class Input(object):
		def __init__(self, name, func, args, outType):
			self.taskName = name
			self.funcRef = func
			self.funcArgs = args
			self.outType = outType
			self.pipedFrom = None
			self.pipeTo = []
			
	def __init__(self):
		self.inputs = {}
		self.pipes = {}

	#@ArrowSentinel.log
	def addInput(self, name, func=None, args=(), expOut=None):
		newInput = self.Input(name, func, args, expOut)
		self.inputs.update({name: newInput})
		#return newInput

	def addPipe(self, piperName, pipeeName, byElem): 
		self.pipes.update({pipeeName: (piperName, byElem)})

	def generateCollectionTable(self):
		import CollectionTable as ctable
		return ctable.CollectionTable(self.inputs, self.pipes)

"""
test = Collect()
from SP500 import scrapeSP500
from DelayedOptionsChain import marketwatchOptionChain 
import pandas as pd

def function(): pass
def funct(): pass

test.addInput(name="scrapeSP500", func=scrapeSP500, expOut=list)
test.addInput(name="optionChain", func=marketwatchOptionChain, expOut=pd.DataFrame)
test.addInput(name="layer3", func=function, expOut=None)
test.addInput(name="layer4", func=funct, expOut=None)

test.addPipe(piperName='scrapeSP500', pipeeName="optionChain", byElem=True)
test.addPipe(piperName='optionChain', pipeeName="layer3", byElem=True)
test.addPipe(piperName='layer3', pipeeName="layer4", byElem=False)

ctable = test.generateCollectionTable()
from CollectionSentinel import CollectionSentinel
csent = CollectionSentinel(ctable.funcs)
print(csent.generateAllCollectionTasks())
"""
