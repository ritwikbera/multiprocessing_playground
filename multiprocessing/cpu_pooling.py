import multiprocessing as mp 

def do_calculation(data):
	return data * 2

def start_process():
	print('Starting {}'.format(mp.current_process().name))

if __name__=='__main__':
	inputs = list(range(30))
	print('Input : {}'.format(inputs))

	builtin_outputs = map(do_calculation, inputs)
	print('Built-in: {}'.format(builtin_outputs))

	pool_size = mp.cpu_count()
	pool = mp.Pool(processes=pool_size, initializer=start_process,)

	pool_outputs = pool.map(do_calculation, inputs)
	pool.close()
	pool.join()

	print('Pool : {}'.format(pool_outputs))