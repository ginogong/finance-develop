class P(object):
	def __init__(self):
		print 'calling Ps constructor'

class C(P):
	def __init__(self):
		super(C,self).__init__()
		print 'calling Cs constructor'

class RoundFloat(float):
	def __new__(cls,val):
		return float.__new__(cls,round(val,2))

class Student(object):
	def __init__(self,name):
		self.name = name

	def __str__(self):
		return 'This is a student  %s' % self.name

	__repr__ = __str__
class Fibo(object):
	def __init__(self):
		self.a, self.b = 0, 1
	def __iter__(self):
		return self 
	def next(self):
		self.a,self.b = self.b, self.a + self.b
		if self.a > 1000:
			raise StopIteration()
		return self.a
	def __getitem__(self,n):
		if isinstance(n, int):

			a,b = 1,1
			for _ in range(n):
				a, b = b , a + b
			return a
		if isinstance(n,slice):
			start = n.start
			stop  = n.stop
			a, b = 1, 1
			l = []
			for x in range(stop):
				if x >= start:
					l.append(a)
				a, b = b , a + b
			return l


def foo(s):
	n = int(s)
	assert n != 0, 'zero err'
	return 10/n

print foo('')
