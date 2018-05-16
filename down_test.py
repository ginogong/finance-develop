#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 09:14:15 2017

@author: Gino
"""

from __future__ import division
import pandas as pd
pd.set_option('max_row',60)
pd.set_option('expand_frame_repr', True)

#strategy args
RISE_RANGE = 0.15
RISE_DAY   = 3
DOWN_DAY_SUM   = 0
DOWN_PCT   = 0.7
CLOSE_RATE = 1.02

#train args
BATCH_DAYS = 40

def down_stragety(df):
    df.index = range(len(df))
    #rise range judge
    rise_range = 0.0
    if len(df) > 10:
        df_start = df[:-2][df['conti_rise'] == 0].tail(1)
        df_end = df[:-2][df['conti_rise'] > 0].tail(1)
        df_start = pd.concat([df_start,df_end])
        df_start.index = range(len(df_start))
        if len(df_start) > 1:
            if df_start.loc[0,'date'] < df_start.loc[1,'date']:
                df_start['change_range'] = df_start.close.pct_change()
                rise_range = df_start.loc[1,'change_range']
                #print df['date'].tail(1),' ',rise_range
                
    rise_range_sig = rise_range > RISE_RANGE
    # rise day num judge
    rise_day = df.loc[list(df.index)[-3],'conti_rise']
    rise_day_sig = rise_day >= RISE_DAY
    #print df['date'].tail(1),' ',rise_day,' ',rise_day_sig
    #down day judge
    t2_down_count = df.loc[list(df.index)[-1],'t2_count']
                           
    down_count_sig = t2_down_count == DOWN_DAY_SUM
    #print df['date'].tail(1),' ', t2_down_count, down_count_sig
    #T-2 T-1 down range judge
    low_price_t2 = df[-3:-1].low.min()
    low_price_t = df[-1:].low.min()
    high_price = df[-4:-2].close.max()
    rise_start_price = high_price / (1 + rise_range)
    t2_low_sig = low_price_t2 > rise_start_price * (1 + rise_range *DOWN_PCT)
    t_low_sig  = low_price_t < rise_start_price * (1 + rise_range *DOWN_PCT)
    #close low rate judge
    close_low_rate_sig = df[-1:].close_low_rate.min() > CLOSE_RATE
    #print df['date'].tail(1),close_low_rate_sig
    #print 'rise_range_sig : ',rise_range_sig
    #print 'rise_day_sig: ' ,rise_day_sig
    #print 'down_count_sig:',down_count_sig
    #print 't2_low_sig:',t2_low_sig
    #print 't_low_sig:',t_low_sig
    #print 'close_low_rate_sig',close_low_rate_sig



    if rise_range_sig and rise_day_sig  and t_low_sig and close_low_rate_sig :
        return df[-1:][['date','close','code']]
    else:
        return None


def back_test(df):
    result = pd.DataFrame(columns=['date','close','code','max_rise','max_down'])
    if len(df) > BATCH_DAYS:
        
        for i in range(len(df) - BATCH_DAYS):
            end = BATCH_DAYS + i
            df_train = df[:end]
            df_temp = down_stragety(df_train)
            if df_temp is not None:
                if end < len(df):
                    df_vali = df[end-1:end+1]
                    df_vali.index = range(len(df_vali))
                    df_vali['max_rise'] = df_vali['high'] / df_vali['close']\
                                        .shift(1) - 1.0
                    df_vali['max_down'] = df_vali['low'] / df_vali['close']\
                                        .shift(1) - 1.0
                    df_temp['max_rise'] = df_vali.loc[1,'max_rise']
                    df_temp['max_down'] = df_vali.loc[1,'max_down']
                else:
                    df_temp['max_rise'] = 0
                    df_temp['max_down'] = 0 
            result = pd.concat([result,df_temp])
    return result
        
    
       
df = pd.read_hdf('dayk_down.h5','dayk_down')

df_group = df.groupby('code')

res = df_group.apply(back_test)
res.to_csv('trend_down_001.csv')

