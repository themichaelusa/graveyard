from Arrow import Arrow

### EXAMPLE FRAME ####

class Frame(Arrow):
	def __init__(self):
		self.name = "test"

	def collect(self):
		
		from SP500 import scrapeSP500
		from DelayedOptionsChain import marketwatchOptionChain 
		import pandas as pd

		addInput(name="scrapeSP500", func=scrapeSP500, expOut=list)
		addInput(name="optionChain", func=marketwatchOptionChain, expOut=pd.DataFrame)
		addPipe(piperName='scrapeSP500', pipeeName="optionChain", byElem=True)

	def process(self):
		pass
	
	def store(self):
		pass

a = Arrow(Frame)
a.run()	