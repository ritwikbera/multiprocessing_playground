
import sys
from time import time

try:
    import torch
except ModuleNotFoundError:
    print('Not in PyTorch virtual environment')
import functools


class Tprofiler:

    def __init__(self):
        pass

    def __enter__(self):
        sys.settrace(self.trace_calls)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.settrace(None)

    def trace_calls(self,frame, event, arg):
        
        if event in ['call', 'line']:
        
            co = frame.f_code
            func_name = co.co_name
            
            if func_name != 'a' and func_name != 'b':
                # Profile only a and b
                return
            
            func_line_no = frame.f_lineno
            func_filename = co.co_filename
            caller = frame.f_back

            try:
                caller_line_no = caller.f_lineno
                caller_filename = caller.f_code.co_filename

                print('Call to {} on line {} of {} from line {} of {}'.format( \
                    func_name, func_line_no, func_filename, caller_line_no, caller_filename))
            
            except AttributeError:    # No proper caller available
                caller_line_no = 0
                caller_filename = 'None'
            finally:
                pass

            if event == 'line':
                print('Function {} is executed at {}'.format(frame.f_code.co_name, time()))
        
        return

def c():
    print('Unprofiled, in c(), ending!')
    return 3

def b():
    print('in b()')
    return 4

def a():
    bo, co = 0, 0
    print('in a()')
    bo = b()
    co = c()
    print(bo+co)


profiler = Tprofiler()
with profiler:
    a()

print('Without profiling')
a()