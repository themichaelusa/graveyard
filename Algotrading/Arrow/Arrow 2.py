class Arrow(object):

	def __init__(self, frame): 
		self.frame = frame

	def run(self, time=None):
		self.frame = self.frame()

		while(True):
			self.frame.collect()
			self.frame.process()
			self.frame.store()





