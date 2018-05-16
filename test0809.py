#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 20:52:33 2017

@author: Gino
"""
from __future__ import division
import pandas as pd 
import numpy as np
import concat_dataframe



def recent_volume_mom(s,num=3):
    return s[-num:].mean()


def coeffienct_of_variance(df):
    return df.close.std()/df.close.mean()


def lower_upper_limit(df,num):    # 计算上下限的值 及上下线距离当前天数
    df.index = range(len(df))
    length = len(df)
    if length < num:              #找出距离当前最少多少天的极值
        min_temp = df.low.min()
        max_temp = df.high.max()
    else:
        min_temp = df[-num:].low.min()
        max_temp = df[-num:].high.max()
    df_min_temp = df[df['low']== min_temp]
    min_len = len(df[df['low']== min_temp])
    days_min = len(df) - df_min_temp.index[min_len-1]
    days_max = len(df) - df[df['high']== max_temp].index[len(df[df['high']== max_temp])-1]
    return min_temp,days_min,max_temp,days_max


def recent_limit(df,num):    #计算上下限函数
    #print df
    if len(df) > 0:             #判断dataframe是否为空
        df.index = range(len(df))
        df_max = df[df['days_max']>num]
        if len(df_max) > 0:
            df_max.index = range(len(df_max))
            maxs = df_max.loc[0,'maxs']
        else:
            maxs = 0
        df_min = df[df['days_min']>num]
        if len(df_min) > 0:
            df_min.index = range(len(df_min))
            mins = df_min.loc[0,'mins']
        else:
            mins = 0
    return maxs,mins

def limit_dataframe(df,days_list):   # 计算dataframe上下限函数
    mins_li = []
    days_mins_li = []
    maxs_li = []
    days_maxs_li = []
    for day in days_list:
        mins,days_mins,maxs,days_maxs = lower_upper_limit(df,day) #计算最高最低与当前距离天数
        mins_li.append(mins)
        days_mins_li.append(days_mins)
        maxs_li.append(maxs)
        days_maxs_li.append(days_maxs)
    #print len(mins_li),len(days_mins_li),len(maxs_li),len(days_maxs_li)
    df_temp = pd.DataFrame({'mins':mins_li,'nums':days_list,\
                       'days_min':days_mins_li,\
                       'maxs':maxs_li,'days_max':days_maxs_li})
    #print df_temp
    return df_temp

def box_postion_ratio(df1,back_days,close_price):  # 计算箱体程序函数
    days_list = [21 ,34, 55, 89, 144, 233, 377]    # 默认计算天数
    df = limit_dataframe(df1,days_list)             #计算dataframe上下限
    recent_upper_limit,recent_lower_limit = recent_limit(df,back_days) #计算近期上下限
    if recent_lower_limit !=0 or recent_upper_limit != 0:
        position_ratio = (close_price - recent_lower_limit)/\
                         (recent_upper_limit - recent_lower_limit)
        box_ratio = (recent_upper_limit - recent_lower_limit)*2 / \
                    (recent_upper_limit + recent_lower_limit)
    else:
        position_ratio = 0
        box_ratio = 0
    return position_ratio, box_ratio

def true_range(df):
    df.index = range(len(df))
    df['hi_lo'] = np.abs((df['high'] - df['low']) / df['close'].shift(1))
    df['hi_cl'] = np.abs((df['high'] - df['close'].shift(1)) / df['close'].shift(1))
    df['cl_lo'] = np.abs((df['close'].shift(1) - df['low']) / df['close'].shift(1))
    df['tr'] = np.max(df[['hi_lo','hi_cl','cl_lo']],axis=1)
    df['tr'].fillna(0,inplace=True)
    return df['tr']

   
def compute(df,last_day):      # 计算函数
    if len(df) > 0:             #先判断df是否为空
        df.index = range(len(df)) # resort index
        days = 55                   #初始化BOX天数
        last_trade_day = df.loc[len(df)-1,'date'] 
        code = df.loc[0,'code']
        if last_trade_day == last_day:
            close_price = df.loc[len(df)-1,'close']            
            pos_ratio ,box_ratio = box_postion_ratio(df,days,close_price) # 计算箱体数值
            if len(df) <55:
                means = true_range(df).mean()
            else:
                means = true_range(df[-days:]).mean()
        else:
            pos_ratio = 0
            box_ratio = 0
            means = 0           
    return pos_ratio,box_ratio,code,means

def box_bottom(dataframe):
    position_upper = 0.2
    position_lower = 0.05
    box      = 0.2
    means    = 0.05
    dataframe = dataframe[(dataframe['position_ratio'] <position_upper )&(dataframe['position_ratio'] >position_lower)]
    dataframe = dataframe[dataframe['box_ratio'] >box]
    dataframe = dataframe[dataframe['mean'] >means ]
    return dataframe

def box_upper(dataframe):
    position_upper = 1
    position_lower = 0.9
    box = 0.2
    dataframe = dataframe[(dataframe['position_ratio'] <position_upper )&(dataframe['position_ratio'] >position_lower)]
    dataframe = dataframe[dataframe['box_ratio'] >box]
    return dataframe
    
    
df = concat_dataframe.concat_dataframe()
last_day = sorted(df['date'].unique())[-1]
df.index = range(len(df))
df_groups = df.groupby('code')
df_temp = df[df['code']=='002567']
#print df_temp
#print compute(df_temp,last_day)


df_re= df_groups.apply(compute,last_day)
index = df_re.index
df_re = pd.DataFrame(df_re.tolist(),columns=['position_ratio','box_ratio','code','mean'])
df_re.index = index
df_bottom = box_bottom(df_re)
df_up = box_upper(df_re)
#print  'bottom:',df_bottom
print  'ceiling,',df_up
'''
df_re.name = 'result'
df3 = pd.DataFrame(df_re)
df3[df3['position_ratio'] <0.2 & df3['box_ratio']>0.2]


df3['position_ratio'] = df3['result'][0]
df3['box_ratio'] = df3['result'][1]

print df3[df3['position_ratio'] <0.2 & df3['box_ratio']>0.2]



df = df[df['date'] >='2017-02-17']
days_li  = [21 ,34, 55, 89, 144, 233, 377]
mins_li = []
maxs_li = []
days_mins_li = []
days_maxs_li = []
code_li = []
date_li = []

for day in days_li:
    mins,days_mins,maxs,days_maxs = lower_upper_limit(df,day)
    mins_li.append(mins)
    days_mins_li.append(days_mins)
    maxs_li.append(maxs)
    days_maxs_li.append(days_maxs)
    
            
df1 = pd.DataFrame({'mins':mins_li,'nums':days_li,'days_min':days_mins_li,'maxs':maxs_li,'days_max':days_maxs_li})


recent_upper_limit,recent_lower_limit = recent_limit(df1,40)
close_today = df.loc[len(df)-1,'close']

position_ratio = (close_today - recent_lower_limit) / \
        (recent_upper_limit - recent_lower_limit)
box_ratio = (recent_upper_limit - recent_lower_limit)*2 / \
        (recent_upper_limit + recent_lower_limit)
print position_ratio
print box_ratio



    cv_temp = coeffienct_of_variance(df_temp)
    print cv_temp
    if cv_temp >= cv_ttl :
        print '{} not in a box'.format(df.loc[i,'date'])
    else:
        df_temp_2 = df[i:i+2 *window_num ]
        cv_temp_2 = coeffienct_of_variance(df_temp_2)
        print cv_temp_2
        if cv_temp < cv_temp_2:
            for j in range(21,1,-1):
                cv_temp_2_min = 0
                cv_temp_2 = coeffienct_of_variance(df[i:i+window_num+j])
                if cv_temp_2 < cv_temp_2_min:
                    index = j
                cv_temp_2_min = min(cv_temp_2,cv_temp_2_min)
                
            if cv_temp_2_min > cv_temp:
                print '{} last from {} to {}'.format(df.loc[i,'date'],df.loc[i,'date'],df.loc[i+window_num+j,'date'])
            else:
                print 'xxx'
                
'''
        


'volume' 

#df['close'].plot()
#df['close'].rolling(window=21,min_periods=1).mean().plot()
#df['close'].rolling(window=21,min_periods=1).var().plot()
#df['close'].plot()

'''
df['volume'].rolling(window=55,min_periods=1).mean().plot() 
df['volume'].rolling(window=55,min_periods=1).std().plot()
    

df['close'].rolling(window=3,min_periods=1).mean().plot()
df['close'].rolling(window=89,min_periods=1).mean().plot()
'''  
'change'
'''   
#print df.rolling(10,min_periods=1).apply(rise_ratio)
df['max_change_10'] = df['close'].rolling(10,min_periods=1).apply(rise_ratio)
df['max_change_20'] = df['close'].rolling(20,min_periods=1).apply(rise_ratio)
df['max_change_30'] = df['close'].rolling(30,min_periods=1).apply(rise_ratio)

df['now_change_10'] = df['close'].rolling(10,min_periods=1).apply(lambda x:x[-1]/x.min())
#df = df[df['date']>='2016-10-30']
#df[['date','max_change_10','max_change_20','max_change_30','now_change_10']].plot()
print df[df['max_change_10']==df['now_change_10']]['date']
'''