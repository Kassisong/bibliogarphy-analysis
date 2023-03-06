#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 16:00:33 2023

@author: songyining
"""

import matplotlib.pyplot as plt
import numpy as np



plt.figure(figsize=(10,6),dpi=500)

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        # 同时显示数值和占比的饼图
        return '{v:d}'.format(p=pct,v=val)
    return my_autopct

col = []
for i in np.arange(0,11):
    col.append(plt.cm.Set3(i))
for i in np.arange(0,5):
    col.append(plt.cm.Set3(i))
# col.append(plt.cm.Set3(3))


country_name=['USA','Canada',
              'England','Germany','Italy','Netherlands','France','Russia','Spain','Poland',
              'Australia',
              'China','India','Japan',
              'South African']
country_num2 = [478,123,
                256,229,145,135,94,79,49,34,
                220,
                125,72,58,
                39]         

continent=[601, 1021, 220, 255,39]
continent_name = ['North America','Europe','Oceania','Asia','African']

plt.title('The article volume of countries',fontsize=20,fontweight='bold')
size = 0.3
p1 = plt.pie(country_num2,
             autopct=make_autopct(country_num2),
             radius=1-size,
             wedgeprops=dict(width=0.3),
             colors=col,
             labels=country_name,
             pctdistance = 0.75,
             labeldistance = 0.9,
             textprops={'fontsize': 8})


color = plt.get_cmap('Blues')(np.linspace(0.8,0.2,len(continent)))
p2 = plt.pie(continent,
             autopct=make_autopct(continent),
             radius=1,
             wedgeprops=dict(width=0.3),
             colors=color,
             labels=continent_name,
             pctdistance = 0.85,
             labeldistance = 1.05,
             textprops={'color': 'navy','fontsize': 15})


plt.legend(loc=0,bbox_to_anchor=(-0.05, 0.99),frameon=False,fontsize=8)

