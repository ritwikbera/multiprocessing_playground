from time import clock
from multiprocessing import Pool
  
def times_two(x):
   return x*2

def lazy_map(xs):
   return list(map(times_two, xs))

def parallel_map(xs, chunk=8500):
   with Pool(2) as P:
     x =  P.map(times_two, xs, chunk)
   return x

N = 10**6
t1 = clock()
lazy_map(range(N))
lm_time = clock() - t1

t1 = clock()
parallel_map(range(N))
par_time = clock() - t1
print("""
-- N = {} --
Lazy map time:      {}
Parallel map time:  {}
""".format(N,lm_time, par_time))