#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:51:20 2017

@author: Gino
"""

from __future__ import division
import pandas as pd 
import seaborn as sns

PATH = '/Users/Gino/workspace/mysite/stock/stock/'
df = pd.read_csv(PATH + '511810_sell_buy_1102.csv')
grouped = df.groupby('price_to_sell')
print grouped.mean()[['profit_count','profit_mean','profit_sum','profit_midtile']]