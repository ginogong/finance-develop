from __future__ import division
import pandas as pd 
import tushare as ts
import rollingmaxdd

df = pd.read_excel('mini_noshield.xls',sheet='mini')
print df 
'''

df = pd.read_hdf('ml.h5','feature')

start = '2015-01-01'
end = '2017-02-10'
num = 30



df = df[df.index>=start]
df = df[df.index<=end]
times = int(round(len(df) / num))

for i in range(times+ 1):
	srt = i * num
	ed  = (i + 1) * num
	df_temp = df[srt:ed]
	print 'this is  %s' % (i+1)
	print df_temp['change']
'''




