# -*- coding:utf-8 -*-
"""
Author : Ronghong Ji
Time   : 2022/11/3
E-mail : jironghong1998@gmail.com
Desc.  :
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

log_file=input("please input the log file:")
f=open(log_file,'r')
lines=f.readlines()
f.close()
new_line=[]
number=[]
for index,line in enumerate(lines):
    line=line.split()
    if 'Step' in line:
        index_1=index
        begin_line=line
        print(index_1)
        print(begin_line)
        continue

    if 'Loop' in line:
        index_2=index
        end_line=line
        print("the calculation is finished!")
        print(index_2)
        print(end_line)
        break
    else:
        index_2=index
        # print("the calculation is not finished")
        # continue
        


for i in range(len(begin_line)):
    begin_line[i]=[]
    for line in lines[index_1+1:index_2]:
        line=line.split()
        begin_line[i].append(float(line[i]))

x = begin_line[0]
y = begin_line[4]

data_dict = {}
for i,j in zip(x,y):
    data_dict[i] = j

plt.xlabel("x-date")
plt.ylabel("y-item")
x = [i for i in data_dict.keys()]
y = [i for i in data_dict.values()]
plt.plot(x, y, "r")
plt.show()
