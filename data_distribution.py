# -*- coding:utf-8 -*-
"""
Author : Ronghong Ji
Time   : 2022/11/11
E-mail : jironghong1998@gmail.com
Desc.  :
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 读取z轴坐标并取出需要的帧数
comfile =  input("please input your file name:")
start = input("please input the start number:")
end = input("please input the end number:")
xyz = pd.read_table(comfile, header=None, delimiter='    ', skiprows=0)
z = xyz[2]
need_z = z[start-1 : end]

# 设置分段区间
bins=[-50,-40,-30,-20,-10,0,10,20,30,40,50]
# 按分段离散化数据
segments=pd.cut(need_z, bins, right=False)
#统计各分段数据个数
counts=pd.value_counts(segments,sort=False)
ave = []

# 绘制柱状图
b=plt.bar(ave.index.astype(str),ave)
# 添加数据标签
plt.bar_label(b,ave)
plt.show()