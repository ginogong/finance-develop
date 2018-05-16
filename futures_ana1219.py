#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 19:26:25 2017

@author: Gino
"""
from __future__ import division
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
PATH = '/Users/Gino/Downloads/'

def relate_avg(df,time_start=5):
    day_start = '09:0'
    time_start = day_start + str(time_start)
    std = df[('09:00:00'<=df['time']) &(df['time']<=time_start)]['diff_abs'].mean()
    df['diff_abs_std'] = df['diff_abs'] - std
    df.index = range(len(df))
    print df['time'].tail(20)
    df[df['time']<'15:00:00']['diff_abs'].plot()
    
    
    

df = pd.read_csv(PATH + 'JM1801J1801.csv')
columns = ['datetime','ftr1','ftr2','diff_abs','diff_relate']
df.columns = columns
df_ana = df[['datetime','diff_abs','diff_relate']]
df_ana[['diff_abs','diff_relate']] =df_ana[['diff_abs','diff_relate']] * 100
df_ana = df_ana[df_ana['diff_abs'] <90] 
df_ana['date'] = df_ana['datetime'].str.split(' ').str.get(0)
df_ana['time'] = df_ana['datetime'].str.split(' ').str.get(1)
df_temp = df_ana[df_ana['date']=='2017-11-30']
relate_avg(df_temp)
'''
df_ana_temp = df_ana[df_ana['date']>'2017-11-21']
df_ana_temp['diff_abs'].plot()
print df_ana.describe()
sns.distplot(df_ana['diff_abs'],kde=False)
'''
