#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 21:52:18 2017

@author: Gino
"""
from dataapi import Client
token = 'f5bcd95440f205e0ecdb8bd6f7fdbb45eb4c868b8729d60a792acb0ef5c4367c'
if __name__ == "__main__":
    try:
        client = Client()
        client.init(token)
        url1='/api/fund/getFundNavJY.json?field=&beginDate=20171001&endDate=20171023&secID=&ticker=511900'
        code, result = client.getData(url1)
        if code==200:
            print result
        else:
            print code
            print result
        url2='/api/equity/getSecST.csv?field=&secID=&ticker=000521&beginDate=20020101&endDate=20150828'
        code, result = client.getData(url2)
        if(code==200):
            file_object = open('thefile.csv', 'w')
            file_object.write(result)
            file_object.close( )
        else:
            print code
            print result
    except Exception, e:
        #traceback.print_exc()
        raise e