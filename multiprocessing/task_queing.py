import multiprocessing as mp 
import time

class Consumer(mp.Process):
	def __init__(self, task_queue, result_queue):
		mp.Process.__init__(self)
		self.task_queue = task_queue
		self.result_queue = result_queue

	def run(self):
		proc_name = self.name
		while True:
			next_task = self.task_queue.get()
			if next_task is None:
				print('Exiting {}'.format(proc_name))
				self.task_queue.task_done()
				break
			print('Process name: {}, Task {}'.format(proc_name, next_task))
			answer = next_task()
			self.task_queue.task_done()
			self.result_queue.put(answer)
		return

class Task(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b 
	def __call__(self):
		time.sleep(0.1)
		return '({}*{} = {})'.format(self.a, self.b, self.a*self.b)
	def __str__(self):
		return '({}*{})'.format(self.a, self.b)

if __name__=='__main__':
	tasks = mp.JoinableQueue()
	results = mp.Queue()

	num_consumers = mp.cpu_count()
	consumers = [Consumer(tasks, results) for x in range(num_consumers)]
	
	for w in consumers:
		w.start()

	num_jobs = 10
	for i in range(num_jobs):
		tasks.put(Task(i, i))

	for i in range(num_consumers):
		tasks.put(None)	

	tasks.join()

	while num_jobs:
		result = results.get()
		print('Result: {}'.format(result))
		num_jobs -= 1		
