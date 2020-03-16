
class task_reference_queue:
	def __init__(self, arg, tasks={}):
		self.tasks = tasks
		self.jobs = []

	def add_task(self, name, ref): 
		self.tasks.update({name:ref})

	def add_job(self, ref_name, *ref_args):
		self.jobs.append((ref_name, ref_args))

	def process_tasks(self, mp=False, asyn=False):
		results = []
		for job in self.jobs:
			func = self.tasks(job[0])
			results.append(func(*job[1]))
		self.jobs.clear()
		return [r for r in results if r is not None]






		