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
        min_temp = df.close.min()
        max_temp = df.close.max()
    else:
        min_temp = df[-num:].close.min()
        max_temp = df[-num:].close.max()
    df_min_temp = df[df['close']== min_temp]
    min_len = len(df[df['close']== min_temp])
    days_min = len(df) - df_min_temp.index[min_len-1]
    days_max = len(df) - df[df['close']== max_temp].index[len(df[df['close']== max_temp])-1]
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
            mins = 1000
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
    if recent_lower_limit !=1000 or recent_upper_limit != 0:
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
        df.index = range(len(df)) # reset index
        days = 21                  #初始化BOX天数
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


def box_upper(dataframe):
    #print dataframe
    if len(dataframe) >0 :
        position_upper = 1
        position_lower = 0.9
        box = 0.25
        dataframe = dataframe[(dataframe['position_ratio'] <position_upper )&(dataframe['position_ratio'] >position_lower)]
        dataframe = dataframe[dataframe['box_ratio'] >box]
    return dataframe
    
    
df = concat_dataframe.concat_dataframe()
last_day = sorted(df['date'].unique())[-1]
df.index = range(len(df))
df_groups = df.groupby('code')
#df_temp = df[df['code']=='000863']
df_re= df_groups.apply(compute,last_day)
#df_re = compute(df_temp,last_day)
df_re = pd.DataFrame(df_re.tolist(),columns=['position_ratio','box_ratio','code','mean'])
df_re.index = range(len(df_re))
df_up = box_upper(df_re)
print  df_up
#print df_re
'''
df_re= df_groups.apply(compute,last_day)
df_re = compute(df_temp,last_day)
index = df_re.index


'''

