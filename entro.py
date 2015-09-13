import math

def entropia(a):
	a = [i/float(sum(a)) for i in a]
	b = [math.log(1/float(i)) for i in a]
	print sum([a[i]*b[i] for i in range(len(a))])

entropia([0.1])
