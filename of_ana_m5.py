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
buy_price = 99.980
sell_price = 100.010
of_list = ['511660','511810','511990','511900']
#columns = ['code','open','close','high','low','vol','amount']
monday_list = []
date_list = []
profit_total_list = []
profit_mean_list  = []
profit_count_list = []
profit_min_list   = []
profit_mid_list   = []
parameter_buy_list = []
parameter_sell_list = []



df = pd.read_hdf(PATH+'of.h5','of')

#df = df[df['date'] > slice_date]
df_temp = df[df['code']=='511900']
df_temp['date'] = pd.to_datetime(df_temp['date'],format='%Y-%m-%d')
df_temp = df_temp.set_index('date')
df_temp['weekday'] = df_temp.index.weekday

#main
#find monday
for i in range(len(df_temp)):
    if list(df_temp.index.weekday)[i] == 0:
        monday_list.append(i)
#run 1week parameter
for buy_price in range(99950,99990,1):
    for sell_price in range(99990,100050,1):
        buy_price_list = []
        buy_day_list = []
        sell_price_list = []
        for num in range(len(monday_list)):

            #print monday_list[num]
            df_slice = df_temp[monday_list[num]:monday_list[num]+3]
            first_week = df_slice[0:3]
            if first_week.low.min() < buy_price/1000.0:
                flag = 0
                buy_price_list.append(buy_price/1000.0)
                
                last_day = list(df_slice.index)[-1]
                for i in df_slice.index:
                    if flag == 0:
                        if df_slice.loc[i,'low'] < buy_price/1000.0:
                            buy_day_list.append(i.strftime('%Y-%m-%d'))
                            flag = 1
                            if df_slice[i:].high.max() > sell_price/1000.0:
                                sell_price_list.append(sell_price/1000.0)
                            else:
                                sell_price_list.append(df_slice.loc[last_day,'close'])
                      
            num += 1

        df_result = pd.DataFrame({'buy_date':buy_day_list,'buy_price':buy_price_list,\
                                  'sell_price':sell_price_list})
        df_result['profit'] = df_result['sell_price'] - df_result['buy_price']
        #print df_result
        profit_total = df_result['profit'].sum()
        profit_mean  = df_result['profit'].mean()
        profit_count = df_result['profit'].count()
        profit_min   = df_result['profit'].min()
        profit_mid   = df_result['profit'].quantile(0.5)
        profit_total_list.append(profit_total)
        profit_mean_list.append(profit_mean)
        profit_count_list.append(profit_count)
        profit_min_list.append(profit_min)
        profit_mid_list.append(profit_mid)
        parameter_buy_list.append(buy_price/1000.0)
        parameter_sell_list.append(sell_price/1000.0)
        print 'buy price :%f, sell price:%f finished!' %(buy_price/1000.0,sell_price/1000.0)

result = pd.DataFrame({'price_to_buy':parameter_buy_list,\
                       'price_to_sell':parameter_sell_list,\
                       'profit_sum':profit_total_list,\
                       'profit_count':profit_count_list,\
                       'profit_mean':profit_mean_list,\
                       'profit_min':profit_min_list,\
                       'profit_midtile':profit_mid_list})

result.to_csv(PATH+'511900_sell_buy_1102.csv') 
        

#判断是否有预设目标之下的买入机会
'''
df_temp['date'] = pd.to_datetime(df_temp['date'],format='%Y-%m-%d')
df_temp = df_temp.set_index('date')
df_weekday = df_temp
df_weekday['weekday'] = df_temp.index.weekday
print df_weekday

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