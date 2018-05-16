#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
from sklearn import neighbors
import threading
import time
#----setting------
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)
#-----------------
k_list = []
class Listadder:
	def __init__(self,lister):
		self.lister = lister

	def adder(self,item):
		self.lister.append(item)
		return self.lister
class Thread_demo(threading.Thread):
	def __init__(self,index):
		threading.Thread.__init__(self)
		self.index = index
	def run(self):
		for i in range(5):
			k_list.append(i)
			print '\nnow is thread %s' % self.index
			print i 
			time.sleep(1)


			

threads = []
for i in range(4):
	thread = Thread_demo(i)
	thread.start()
	threads.append(thread)

for t in threads:
	t.join()
print k_list

