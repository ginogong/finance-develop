# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np 

def f(x,y):
	return 10 * x + y

l1 = np.linspace(1,10,10)
weights = np.ones(3) / 3.0
sma = np.convolve(weights,l1)[2:-2]
deviation = []
C = len(l1)
A = np.zeros((4,4),float)
for i in range(4):
	A[i,] = l1[-4-1-i:-1-i]
b = l1[-4:]
b = b[::-1]
(x, residuals ,rank, s) = np.linalg.lstsq(A,b)
print np.arange(9)
print b
'''
int sma
for i in range(2,C):
	if i + 3 < C:
		dev = l1[i:i + 3]
		print dev
	else:
		dev = l1[-3:]
	averages = np.zeros(3)
	averages.fill(sma[i-3-1])
	dev = dev -averages
	dev = dev ** 2
	dev = np.sqrt(np.mean(dev))
	deviation.append(dev)
	print deviation
'''

