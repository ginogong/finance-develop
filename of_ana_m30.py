#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 20:17:12 2017

@author: Gino
"""
from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def slice_whole_week(dataframe):
    standard_week = [0,1,2,3,4]
    if list(dataframe.index) == standard_week:
        return 1
    else :
        return 0 
def slice_fri_mon(dataframe):
    fri_mon = [4,0]
    if list(dataframe.index) == fri_mon:
        return 1
    else:
        return 0
def find_next_monday(df,index_num):
    pass

def monday_open_thurday_open(df_slice):
    price_change = df_slice.loc[3,'open'] - df_slice.loc[0,'open']
    return price_change    

def monday_open_thurday_high(df_slice):
    price_change = df_slice.loc[3,'high'] - df_slice.loc[0,'open']
    return price_change

def monday_low_thurday_high(df_slice):
    price_change = df_slice.loc[3,'high'] - df_slice.loc[0,'low']
    return price_change
    
def friday_open_monday_open(df_slice):
    price_change = df_slice.loc[0,'open'] - df_slice.loc[4,'open']
    return price_change


    
PATH = '/Users/Gino/workspace/mysite/stock/stock/'
start_date = '2015-01-01'
end_date = '2017-10-25'
slice_date = '2017-01-01'
of_list = ['511660','511810','511990','511900']
columns = ['date','open','close','high','low','volume','code']
monday_list = []
mon_open_thu_open_list = []
mon_open_thu_high_list = []
mon_low_thu_high_list = []
fri_open_mon_open_list = []


df = pd.read_hdf(PATH+'of.h5','of_M30')
#df = df[df['date'] > slice_date]
df_temp = df[df['code']=='511990']
df_temp['date'] = pd.to_datetime(df_temp['date'],format='%Y-%m-%d')
df_temp = df_temp.set_index('date')
df_weekday = df_temp
df_weekday['weekday'] = df_temp.index.weekday
print df_weekday
'''
for i in range(len(df_weekday)):
    if list(df_weekday.index)[i] == 0:
        monday_list.append(i)

for num in range(len(monday_list)):
    #print monday_list[num]
    df_slice = df_weekday[monday_list[num]:monday_list[num]+5]
    df_slice_fri_mon = df_weekday[monday_list[num]-1:monday_list[num]+1]
    #print df_slice_fri_mon
    if slice_whole_week(df_slice) == 1:
        price_open_open = monday_open_thurday_open(df_slice)
        price_open_high = monday_open_thurday_high(df_slice)
        price_low_high  = monday_low_thurday_high(df_slice)
        mon_open_thu_open_list.append(price_open_open)
        mon_open_thu_high_list.append(price_open_high)
        mon_low_thu_high_list.append(price_low_high)
    if slice_fri_mon(df_slice_fri_mon) == 1:
        price_fri_mon = friday_open_monday_open(df_slice_fri_mon)
        fri_open_mon_open_list.append(price_fri_mon)
        
    num += 1

df_mon_thu = pd.DataFrame({'price_open_open':mon_open_thu_open_list,'price_open_high':mon_open_thu_high_list,\
                           'price_low_high':mon_low_thu_high_list})
df_fri_mon = pd.DataFrame({'price_fri_mon':fri_open_mon_open_list})
print df_mon_thu.describe()
sns.distplot(df_mon_thu['price_low_high'])
sns.plt.show()
#print df_mon_thu.describe()
'''