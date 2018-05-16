#-*- coding:utf-8 -*-
from __future__ import division
import pandas as pd 
import numpy as np 
import tushare as ts
import warnings
from sklearn import neighbors
#----setting------
warnings.filterwarnings('ignore')
#pd.set_option('display.mpl_style','default')
pd.set_option('precision',6)
pd.set_option('expand_frame_repr',False)
#-----------------
 