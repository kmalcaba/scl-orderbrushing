# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 14:48:38 2020

@author: Kirsten
"""

import pandas as pd
import numpy as np

orders = pd.read_csv('./input/order_brush_order.csv').sort_values(by=['shopid', 'event_time'])
orders[['date','time']] = orders['event_time'].str.split(" ", expand=True)
orders['event_time'] = pd.to_datetime(orders['event_time'], errors='coerce')

#filter shop ids with more than 3 orders
filtered_orders = orders.groupby(['shopid', 'userid']).filter(lambda group:len(group)>=3)
#print(filtered_orders.head(-5))
print(filtered_orders.loc[filtered_orders['shopid']==208696908])

filtered_orders = filtered_orders.groupby(pd.Grouper(key='event_time', freq='1H')).filter(lambda group:len(group)>=3)
#list of shop id with possible order brushing
shop_list = filtered_orders.shopid.unique()
print(len(shop_list))

#list of shop id with no order brushing (from initial filtering)
no_brush_shop = np.setdiff1d(orders.shopid.unique(), shop_list)
#print(len(no_brush_shop))

brush = dict((shop, []) for shop in shop_list)

for shop in shop_list:
    shop_orders = filtered_orders.loc[filtered_orders['shopid']==shop]
    order_count = shop_orders.groupby(pd.Grouper(key='event_time', freq='1H')).filter(lambda group:len(group)>=3)
    if not order_count.empty:
        brush[shop].append(order_count.userid.unique())

print(brush)
#final output array
#result = pd.DataFrame({'shopid':list()})
