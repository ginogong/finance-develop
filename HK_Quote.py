#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 12:00:45 2018

@author: Gino
"""
from __future__ import division
import pandas as pd 
import numpy as np
import warnings 
import tushare as ts
from pyquery import PyQuery as pq
import re
import requests
import datetime
import Tkinter

header_req = {
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
               AppleWebKit/537.36 (KHTML, like Gecko) \
               Chrome/45.0.2454.101 Safari/537.36',              
              }
url = 'http://hq.sinajs.cn/list='
code = 'sz300431'
response = requests.get(url + code, headers=header_req)
res_list = response.text.split(',')
cur_time = res_list[31]
cur_date = res_list[30]
open_price = float(res_list[1])
close_price_lastday = float(res_list[2])
current_price = float(res_list[3])
high_price = float(res_list[4])
low_price  = float(res_list[5])
#b1_price   = float(res_list[6])
#a1_price   = float(res_list[7])
current_quanity = float(res_list[8]) / 100    # 100 per unit
current_amount  = float(res_list[9]) /10000  # 10000 per unit
b1_volume = float(res_list[10]) / 100
b1_price  = float(res_list[11])
b2_volume = float(res_list[12]) / 100
b2_price  = float(res_list[13])
b3_volume = float(res_list[14]) / 100
b3_price  = float(res_list[15])
b4_volume = float(res_list[16]) / 100
b4_price  = float(res_list[17])
b5_volume = float(res_list[18]) / 100
b5_price  = float(res_list[19])
a1_volume = float(res_list[20]) / 100
a1_price  = float(res_list[21])
a2_volume = float(res_list[22]) / 100
a2_price  = float(res_list[23])
a3_volume = float(res_list[24]) / 100
a3_price  = float(res_list[25])
a4_volume = float(res_list[26]) / 100
a4_price  = float(res_list[27])
a5_volume = float(res_list[28]) / 100
a5_price  = float(res_list[29])

ask_total_quantity = a1_volume + a2_volume + a3_volume + a4_volume + a5_volume
bid_total_quantity = b1_volume + b2_volume + b3_volume + b4_volume + b5_volume
if ask_total_quantity == 0.0:
    sts_sell_price = 0.00
else :
    sts_sell_price = round(( a1_volume * a1_price + a2_volume * a2_price +
                      a3_volume * a3_price + a4_volume * a4_price +
                      a5_volume * a5_price) /  ask_total_quantity,3)
if bid_total_quantity == 0.0:
    sts_buy_price = 0.00
else :
    sts_buy_price = round(( b1_volume * b1_price + b2_volume * b2_price +
                      b3_volume * b3_price + b4_volume * b4_price +
                      b5_volume * b5_price) /  bid_total_quantity ,3)

dist_to_press = round((sts_sell_price - current_price) * 100 / close_price_lastday , 4)
dist_to_support = round((current_price -sts_buy_price )* 100 /close_price_lastday ,4 )
ab_ratio  = round((bid_total_quantity -ask_total_quantity)   * 100/  (ask_total_quantity + bid_total_quantity),4)
#frame
root = Tkinter.Tk()
root.title('Quote Analysis')
root.geometry('450x400')

title_price = Tkinter.Label(root,text='Price')
title_volume = Tkinter.Label(root,text='Volume')
title_price.grid(row=0,column=1)
title_volume.grid(row=0,column=2)

A5_name = Tkinter.Label(root,text='sell5')
A5_price = Tkinter.Label(root,text=str(a5_price))
A5_volume = Tkinter.Label(root,text=str(a5_volume))
A5_name.grid(row=1,column=0)
A5_price.grid(row=1,column=1)
A5_volume.grid(row=1,column=2)

A4_name = Tkinter.Label(root,text='sell4')
A4_price = Tkinter.Label(root,text=str(a4_price))
A4_volume = Tkinter.Label(root,text=str(a4_volume))
A4_name.grid(row=2,column=0)
A4_price.grid(row=2,column=1)
A4_volume.grid(row=2,column=2)

A3_name = Tkinter.Label(root,text='sell3')
A3_price = Tkinter.Label(root,text=str(a3_price))
A3_volume = Tkinter.Label(root,text=str(a3_volume))
A3_name.grid(row=3,column=0)
A3_price.grid(row=3,column=1)
A3_volume.grid(row=3,column=2)

A2_name = Tkinter.Label(root,text='sell2')
A2_price = Tkinter.Label(root,text=str(a2_price))
A2_volume = Tkinter.Label(root,text=str(a2_volume))
A2_name.grid(row=4,column=0)
A2_price.grid(row=4,column=1)
A2_volume.grid(row=4,column=2)

A1_name = Tkinter.Label(root,text='sell1')
A1_price = Tkinter.Label(root,text=str(a1_price))
A1_volume = Tkinter.Label(root,text=str(a1_volume))
A1_name.grid(row=5,column=0)
A1_price.grid(row=5,column=1)
A1_volume.grid(row=5,column=2)

B1_name = Tkinter.Label(root,text='buy1')
B1_price = Tkinter.Label(root,text=str(b1_price))
B1_volume = Tkinter.Label(root,text=str(b1_volume))
B1_name.grid(row=6,column=0)
B1_price.grid(row=6,column=1)
B1_volume.grid(row=6,column=2)

B2_name = Tkinter.Label(root,text='buy2')
B2_price = Tkinter.Label(root,text=str(b2_price))
B2_volume = Tkinter.Label(root,text=str(b2_volume))
B2_name.grid(row=7,column=0)
B2_price.grid(row=7,column=1)
B2_volume.grid(row=7,column=2)

B3_name = Tkinter.Label(root,text='buy3')
B3_price = Tkinter.Label(root,text=str(b3_price))
B3_volume = Tkinter.Label(root,text=str(b3_volume))
B3_name.grid(row=8,column=0)
B3_price.grid(row=8,column=1)
B3_volume.grid(row=8,column=2)

B4_name = Tkinter.Label(root,text='buy4')
B4_price = Tkinter.Label(root,text=str(b4_price))
B4_volume = Tkinter.Label(root,text=str(b4_volume))
B4_name.grid(row=9,column=0)
B4_price.grid(row=9,column=1)
B4_volume.grid(row=9,column=2)

B5_name = Tkinter.Label(root,text='buy5')
B5_price = Tkinter.Label(root,text=str(b5_price))
B5_volume = Tkinter.Label(root,text=str(b5_volume))
B5_name.grid(row=10,column=0)
B5_price.grid(row=10,column=1)
B5_volume.grid(row=10,column=2)

stats_name = Tkinter.Label(root,text='Statistics')
stats_name.grid(row=0,column=5)

weighted_sell_price_name = Tkinter.Label(root,text='weighted_sell_price')
weighted_sell_price = Tkinter.Label(root,text=str(sts_sell_price))
weighted_sell_price_name.grid(row=1,column=4)
weighted_sell_price.grid(row=1,column=5)

weighted_buy_price_name = Tkinter.Label(root,text='weighted_buy_price')
weighted_buy_price = Tkinter.Label(root,text=str(sts_buy_price))
weighted_buy_price_name.grid(row=2,column=4)
weighted_buy_price.grid(row=2,column=5)
 
dist_to_pressure_name = Tkinter.Label(root,text='dist_to_press')
dist_to_pressure = Tkinter.Label(root,text=str(dist_to_press)+'%')
dist_to_pressure_name.grid(row=3,column=4)
dist_to_pressure.grid(row=3,column=5)

dist_to_support_name = Tkinter.Label(root,text='dist_to_support')
dist_to_support = Tkinter.Label(root,text=str(dist_to_support)+'%')
dist_to_support_name.grid(row=4,column=4)
dist_to_support.grid(row=4,column=5)

ab_ratio_name = Tkinter.Label(root,text='ab_ratio')
ab_ratio = Tkinter.Label(root,text=str(ab_ratio)+'%')
ab_ratio_name.grid(row=5,column=4)
ab_ratio.grid(row=5,column=5)


root.mainloop()
