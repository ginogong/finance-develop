#*-* coding:utf-8 *-*
from __future__ import division
import pandas as pd 
import tushare as ts
import tensorflow as tf
import numpy as np 
import warnings
import datetime
import seaborn
warnings.filterwarnings('ignore')
'''
g1 = tf.Graph()
with g1.as_default():
	v = tf.get_variable('v',initializer=tf.zeros_initializer(shape=[1]))

g2 = tf.Graph()
with g2.as_default():
	v = tf.get_variable('v',initializer=tf.ones_initializer(shape=[1]))

with tf.Session(graph=g1) as sess:
	tf.initialize_all_variables().run()
	with tf.variable_scope('',reuse=True):
		print sess.run(tf.get_variable('v'))

with tf.Session(graph=g2) as sess:
	tf.initialize_all_variables().run()
	with tf.variable_scope('',reuse=True):
		print sess.run(tf.get_variable('v'))

w1 = tf.Variable(tf.random_normal([2,3],stddev=2,seed=1))
w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
x = tf.constant([[0.7,0.9]])

init_op = tf.initialize_all_variables()
a = tf.matmul(x,w1)
b = tf.matmul(a,w2)
sess = tf.Session()
sess.run(init_op)

print sess.run(b)
sess.close()


from numpy.random import RandomState

batch_size = 8
w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
x = tf.placeholder(tf.float32,shape=(None,2),name='x-input')
y_ = tf.placeholder(tf.float32,shape=(None,1),name='y-input')
a = tf.matmul(x,w1)
y = tf.matmul(a,w2)
cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y,1e-10,1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size,2)
Y = [[int(x1+x2 < 1)] for (x1,x2) in X]

with tf.Session() as sess:
	init_op = tf.initialize_all_variables()
	sess.run(init_op)
	print sess.run(w1)
	print sess.run(w2)

	STEPS = 5000
	for i in range(STEPS):
		start = ( i * batch_size) % dataset_size
		end = min(start + batch_size, dataset_size)
		sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
		if i % 1000 == 0:
			total_cross_entropy = sess.run(cross_entropy, feed_dict={x:X,y_:Y})
			print 'After %d training step(s),cross entropy on all data is %g' % (i, total_cross_entropy)
	print sess.run(w1)
	print sess.run(w2)		


def sigmoid(inX):
	return 1.0/(1 + np.exp(-inX))

def stocGradAscent(dataMatrix, classLabel , numIter=150):
	m,n = np.shape(dataMatrix)
	weights = np.ones(n)
	for j in range(numIter):
		dataIndex = range(m)
		for i in range(m):
			alpha = 4 /(1.0 + j + i) + 0.01
			randIndex = int(np.random.uniform(0, len(dataIndex)))
			h = sigmoid(dataMatrix[randIndex] * weights)
			error = classLabel[randIndex] - h
			weights = weights + alpha * error * dataMatrix[randIndex]
			del(dataIndex[randIndex])
	return weights

def classifyVector(inX, weights):
	prob = sigmoid(np.sum(inX * weights))
	if prob > 0.5 :
		return 1.0
	else:
		return -1.0

def test():
	hs_list = ['all_hs_change','all_zz_change','hs_zz_amp20','hs_zz_chg10','hs_zz_sma40','hs_zz_vol40']
	zz_list = ['all_hs_change','all_zz_change','hs_zz_amp40','hs_zz_chg20','hs_zz_sma10','hs_zz_vol10']
	df1 = pd.read_hdf('ml.h5','feature002')
	df1 = df1[zz_list]
	df1 = np.array(df1)
	df2 = pd.read_hdf('ml.h5','label002')
	df_hs = df2['hs_cls1']
	df_hs = np.array(df_hs)
	df_zz = df2['zz_cls1']
	df_zz = np.array(df_zz)
	trainWeights = stocGradAscent(df1,df_zz,500)
	errorCount = 0
	numTestVec = 0.0
	for i in range(len(df1)):
		numTestVec += 1.0
		lineArr = []
		if int(classifyVector(df1[i],trainWeights)) != int(df_hs[i]):
			errorCount += 1
	errorRate = float(errorCount) / numTestVec
	print 'the error rate of this test is : %f' % errorRate	
	return  errorRate

def muliTest():
	numTests = 10
	errorSum = 0.0
	for k in range(numTests):
		errorSum += test()
	print 'after %d interations the average error rate is : %f' %(numTests , errorSum / float(numTests))

muliTest()
'''

#df = ts.get_stock_basics()
li = ['code','pe','outstanding','totals','totalAssets','liquidAssets', 'fixedAssets',\
		'reserved','reservedPerShare','esp','bvps','pb','undp','perundp',\
		'rev','profit','gpr','npr','holders','timeToMarket'] 
'''
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
esp,每股收益
bvps,每股净资
pb,市净率
timeToMarket,上市日期
undp,未分利润
perundp, 每股未分配
rev,收入同比(%)
profit,利润同比(%)
gpr,毛利率(%)
npr,净利润率(%)
holders,股东人数

df = pd.read_csv('stock_basic_0508.csv')
print len(df[df['pe'] < 20]['code'])


df = ts.get_k_data(code='600000',start='2017-03-23',end='2017-05-08')
print df.ix[81,'volume'] / df['volume'].mean()

df = pd.read_hdf('dayk.h5','dayk')
now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d')
df_now = df[df['date'] >= '2017-05-08']

print len(df_now)

df = pd.read_hdf('all_index.h5','all_a')
df = df.set_index('date')
df.to_hdf('all_index.h5','all_a')
print df 

df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
                          'foo', 'bar', 'foo', 'foo'],
                   'B' : ['one', 'one', 'two', 'three',
                         'two', 'two', 'one', 'three'],
                   'C' : np.random.randn(8),
                   'D' : np.random.randn(8)})
def get_letter_type(letter):
	if letter.lower() in 'aeiou':
		return 'vowel'
	else:
		
		return 'consonant'

df3 = pd.DataFrame({'X' : ['A', 'B', 'A', 'B'], 'Y' : [1, 4, 3, 2]})
print df.groupby(get_letter_type,axis=1).groups

df = pd.read_hdf('dayk.h5','dayk')
print df[-5:]

df_day = pd.read_hdf('dayk.h5','dayk')
groups = df_day.groupby('code')

close = lambda x:x / x.shift(1) - 1.0
key = lambda x: x.year
zscore = lambda x: (x - x.mean()) / x.std()
fi_na = lambda x: x.fillna(x.mean())
index = pd.date_range('2000-01-01',periods=1000)

trans = groups['close'].transform(close)
df_day['change'] = trans

df_dayk = pd.read_hdf('dayk.h5','dayk')
df = pd.DataFrame({'A': [1] * 10 + [5] * 10,'B':np.arange(20)})

df = pd.DataFrame({'date':pd.date_range('2017-01-01',periods=4,freq='W'),
					 'group':[1,1,2,2],'val':[4,5,6,7]}).set_index('date')
print df.groupby('group').resample('1D').bfill()


df_day = pd.read_hdf('dayk.h5','dayk')
print df_day.groupby('code').close.mean()

df = pd.DataFrame(np.random.randn(1000,3),index=pd.date_range('2000-01-01',periods=1000),columns=['A','B','C'])
df.iloc[::2] = np.nan
print df.groupby(lambda x:x.year).ffill() == df.groupby(lambda x:x.year).fillna(method='ffill')

s1 = pd.Series([1,4,8,10,19,28,20,3,5,7])
s2 = pd.Series(list('ababababab'))
group = s1.groupby(s2)
print group.nlargest(2)
print group.nsmallest(2)

df_day = pd.read_hdf('dayk.h5','dayk')
grouped = df_day.groupby('code')['close']
def f(group):
	return pd.DataFrame({'change':group / group.shift(1) - 1.0})

print grouped.apply(f)

data = pd.Series(np.random.randn(1000))
factor = pd.qcut(data,[0,0.25,0.5,0.75,1.0])

print data.groupby(factor).mean()

np.random.seed(123)
df = pd.DataFrame(np.random.randn(50,2))
df['g'] = np.random.choice(['A', 'B'] , 50)

df.loc[df['g'] == 'B' , 1] += 3
df.groupby('g').boxplot()
print df 

df = pd.DataFrame({'a':[1,0,0], 'b':[0,1,0], 'c':[1,0,0], 'd':[2,3,4]})
print df.groupby(df.sum(), axis=0).sum()
print df 

df = pd.DataFrame({
					'a':  [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
					'b':  [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
					'c':  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
					'd':  [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
					})

def compute(ser):
	res = {'b_sum':ser['b'].sum(), 'c_mean':ser['c'].mean()}
	return pd.Series(res,name='result')

print type(df.groupby('a').apply(compute).stack())

df_day = pd.read_hdf('dayk.h5','dayk')
df_day = df_day[df_day['date'] > '2017-01-01']
grouped = df_day.groupby('code')['close']
df_temp = df_day[df_day['code'] == '603578']

print df_day[df_day['code'] == '603578']

df_day = pd.read_hdf('dayk.h5','dayk')

df_day = df_day.sort_values(by='code')
df_temp = df_day[-1000:]
df_temp = df_temp.sort_values(by='date')
df_temp.index = range(len(df_temp))
pct = lambda x: x / x.shift(1) - 1.0
df_temp['change'] =  df_temp.groupby('code').close.pct_change()
print df_temp
'''
df = pd.read_hdf('all_index.h5' , 'all_a')
seaborn.distplot(df['all_a'])




