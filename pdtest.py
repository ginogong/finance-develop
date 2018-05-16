import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import itertools
import functools

app = 'PRISMA'
data = {'AAA':[4,5,6,7],'BBB':[10,20,30,40],'CCC':[100,50,-30,-50],'DDD':['snowrain','sunny','snow','raining']}
df = pd.DataFrame(data)
long_str = df['DDD'].str.len()>6
df_columns = zip(df.columns,[type(x) for  x in df.ix[0,:]])
query1 = df.query('(CCC> -40 )& (CCC< 60)')
group = df.groupby(['CCC']).sum()
group1 = df.groupby(['CCC']).aggregate(np.sum)
df.AAA.value_counts().plot(kind='bar')
df_mask = pd.DataFrame({'AAA':[True]*4, 'BBB':[False]*4, 'CCC':[True,False]*2})
df1 = df.copy()
df2 = df.copy()
df3 = df.copy()
pf = pd.Panel({'df1':df1,'df2':df2,'df3':df3})
source_col = df.columns
new_col = [str(x) + '_cat' for x in source_col]
categories = {1:'alpha', 2:'beta', 3:'charlie'}
#df.columns = pd.MultiIndex.from_tuples([c.split("_") for c in new_col])
index = list(itertools.product(['Ada','Quinn','Violet'],['Comp','Math','Sci']))
l = 'cat dog cat fish dog cat cat'.split()
l1 = list('aabbccddeeffsaa')
l2 = [True] * 3 + [False]* 4
df4 = pd.concat([df1,df2,df3],ignore_index=True)

df5 = pd.Series([i/100.0 for i in range(11)])
def cumret(x,y):
	return x * (1+y)
def red(x):
	return reduce(cumret,x,1)

df6 = pd.DataFrame({'A' : [1, 1, 2, 2], 'B' : [1, -1, 1, 2]})
gb = df6.groupby('A')
def replace(g):
	mask = g < 0
	print mask
	g.loc[mask] = g[~mask].mean()
	return g
df7 = pd.DataFrame({'code': ['foo', 'bar', 'baz'] * 2,
					'data': [0.16, -0.21, 0.33, 0.45, -0.59, 0.62],
					'flag': [False, True] * 3})
code_group = df7.groupby('code')
agg_b_sort_order = code_group[['data']].transform(sum).sort_values(by='data')
sort_df = df7.ix[agg_b_sort_order.index]
rng = pd.date_range(start='2016-01-01',periods=10,freq='2min')
ts = pd.Series(list(range(10)), index=rng)
def mycust(x):
	print x
	if len(x) > 2:
		return x[1] * 1.234
	return pd.NaT
mhc = {'mean':np.mean, 'max':np.max, 'custom':mycust}
df8 = pd.DataFrame({'host':['other','other','that','this','this'],
					'service':['mail','web','mail','mail','web'],
					'no':[1, 2, 1, 2, 1]}).set_index(['host', 'service'])

mask = df8.groupby(level=0).agg('idxmax')
df9 = pd.DataFrame(data={'case':['A','A','A','B','A','A','B','A','A'],'data':np.random.randn(9)})
dfs = zip(df9.groupby(1* df9['case']=='B'))
df10 = pd.DataFrame({'Province':['ON','QC','BC','AL','AL','MN','ON'],
					'City':['Toronto','Montreal','Vancouver','Calgary','Edmonton','Winnipeg','Windsor'],
					'Sales':[13,6,16,8,4,3,1]})
table1 = pd.pivot_table(df10,values=['Sales'],index=['Province'],columns=['City'],aggfunc=np.sum,margins=True)
df11 = pd.DataFrame(data={'A' : [[2,4,8,16],[100,200],[10,20,30]], 'B' : [['a','b','c'],['jj','kk'],['ccc']]},index=['I','II','III'])
def SeriesFromSubList(alist):
	return pd.Series(alist)

df_orgz = pd.concat(dict([ (ind,row.apply(SeriesFromSubList)) for ind,row in df11.iterrows() ]))

df12 = pd.Series([1,1,1,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4])
df13 = pd.DataFrame(np.random.randn(5,2),columns=['a','b'])
df14 = pd.DataFrame(np.random.randn(6,2),columns=['a','b'],index=np.arange(2,8))
def x_plus_y_divide(x,y,divide=2):
	return (x+y)/divide
df15 = pd.DataFrame(np.random.randn(10,8),columns=list('abcdefgh'))
l1 = [1,2,3,1,2,3]
sf = pd.Series([1,2,3,10,20,30],l1)
print sf.groupby(level=0).first()
