import pandas as pd 

df = pd.read_hdf('dayk.h5','dayk')
print df.tail(10)