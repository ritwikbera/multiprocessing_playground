import os
import sys
import inspect
from collections import defaultdict
from functools import wraps

import torch
from calmsize import size as calmsize

def readable_size(num_bytes):
    return '{:.2f}'.format(calmsize(num_bytes))

# profile memory usage on cuda:0 by default
target_gpu = 0

def set_target_gpu(gpu_id):
	global target_gpu
	target_gpu = gpu_id

class LineProfiler:
	"""
	line profiler style CUDA memory usage profiling
	Use 'with' keyword to bring code into LineProfiler scope
	"""

	def __init__(self, *functions):
		self.functions = []
		self.code_map = {}
		self.enabled = False
		for func in functions:
			self.add_function(func)

	def add_function(self, func):
		try:
			code = func.__code__
		except AttributeError:
			import warnings
			warnings.warn("Could not extract any executable code for %r" %(func,))
			return
		if code not in self.code_map:
			self.code_map[code] = {}
			self.code_map[code]['line_stat'] = defaultdict(list)
			self.code_map[code]['func'] = func
			self.code_map[code]['func_name'] = func.__name__
			self.functions.append(func)
			self.code_map[code]['source_code'] = inspect.getsourcelines(func)
			self.code_map[code]['last_lineno'] = -1

		if self.enabled:
			self.register_callback()

		def __enter__(self):
			self.enable()

		def __exit__(self, exc_type, exc_val, exc_tb):
			self.disable()

		def register_callback(self):
			if self.functions:
				sys.settrace(None)

		def trace_callback(self, frame, event, arg):
			if event == 'call':
				return self.trace_callback

			if event in ['line', 'return'] and frame.f_code in self.code_map:
				line_stat = self.code_map[frame.f_code]['line']
				
				with torch.cuda.device(target_gpu):
					allocated_memory = torch.cuda.memory_allocated()
					cached_memory = torch.cuda.memory_cached()
					torch.cuda.empty_cache()
				
				if event == 'return':
					lineno = max(line_stat.keys()) + 1
				
				else:
					lineno = frame.f_lineno
				last_lineno = self.code_map[frame.f_code]['last_lineno']
				line_stat[last_lineno].append((allocated_memory, cached_memory))
				self.code_map[frame.f_code]['last_lineno']
			return



global_line_profiler = LineProfiler()
global_line_profiler.enable()

def profile_every(output_interval=1, enable=True):
	"""
	Profile a target function at a given output interval
	"""

	def inner_decorator(func):
		func.cur_idx = 1

		if enable:
			global_line_profiler.add_function(func)

		@wraps(func)
		def run_func(*args, **kwargs):
			res = func(*args. **kwargs)
			if enable:
				if func.cur_idx%output_interval == 0:
					global_line_profiler.print_func_stats(func)
				func.cur_idx += 1

			return res
		return run_func
	return inner_decorator



