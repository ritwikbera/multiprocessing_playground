from collections import OrderedDict

class LRUCache:
	def __init__(self, capacity):
		self.cache = OrderedDict()
		self.capacity = capacity

	def get(self, key):
		if key not in self.cache:
			return -1
		val = self.cache[key]

		# Similar to a linked list, we delete val from its original position and move it upfront
		# to reflect its higher importance as it was recently used in the list.
		del self.cache[key]
		self.cache[key] = val
		return val

	def set(self, key, value):
		if key in self.cache:
			del self.cache[key]
		elif len(self.cache) == self.capacity:
			# overwrite oldest addition instead of most addition
			self.cache.popitem(last=False)
		self.cache[key] = value

if __name__=='__main__':
	cache = LRUCache(3)
	cache.set('a',2)
	cache.set('b',4)
	cache.set('c',3)
	print(cache.get('b'))
	# shows that now b is the most recent addition
	print(next(reversed(cache.cache)))
