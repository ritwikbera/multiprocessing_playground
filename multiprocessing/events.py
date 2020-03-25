import multiprocessing as mp 

def producer(ns, event):
	ns.value = 'This is the value'
	event.set()

def consumer(ns, event):
	try:
		value = ns.value
	except Exception as e:
		print('Before event, consumer got {}'.format(str(e)))
	event.wait()
	print('After event, consumer got: {} '.format(ns.value))

if __name__=='__main__':
	mgr = mp.Manager()
	namespace = mgr.Namespace()
	event = mp.Event()
	p = mp.Process(target=producer, args=(namespace, event))
	c = mp.Process(target=consumer, args=(namespace, event))

	c.start()
	p.start()

	c.join()
	p.join()