#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:44:28 2017

@author: Gino
"""

import pandas as pd 
PATH = '/Users/Gino/workspace/mysite/stock/stock/'



def concate_dataframe():
    df_09_13 = pd.read_hdf(PATH + 'dayk_09_14.h5','dayk_09_14')
    df_14_16 = pd.read_hdf(PATH + 'dayk_14_16.h5','dayk_14_16')
    df_17    = pd.read_hdf(PATH + 'dayk_17.h5','dayk_17')
    df_09_13 = df_09_13.append(df_14_16)
    df_09_13 = df_09_13.append(df_17)
    df_09_13 = df_09_13.sort_values(by='date')
    return df_09_13
    
