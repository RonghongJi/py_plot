# -*- coding:utf-8 -*-
"""
Author : Ronghong Ji
Time   : 2022/11/10
E-mail : jironghong1998@gmail.com
Desc.  :
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

def Read_Plot_XPM(fname):
    color, x, y, arr, value_list = {}, [], [], [], []
    title, legend, xlabel, ylabel = '', '', '', ''
    ss = ['Coil', 'B-Sheet', 'B-Bridge', 'Bend', 'Turn', 'A-Helix', '5-Helix', '3-Helix', 'Chain_Separator']
    color_map = [(1, 1, 1), (1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (0.7, 0.3, 0.8), (0.5, 0.5, 0.5), (0, 0.5, 0.5)]
    with open(fname, 'r') as f:
        line = f.readline().rstrip('\n')
        while line:
            if 'title' in line:
                title  = line.split('"')[1] 
            elif 'legend' in line:
                legend = line.split('"')[1]
            elif 'x-label' in line:
                xlabel = line.split('"')[1]
            elif 'y-label' in line:
                ylabel = line.split('"')[1]
            #矩阵维度dim[0]*dim[1], nframe * nres
            elif 'static char' in line:
                dim = np.array(f.readline().split('"')[1].split(), dtype=int)
                for i in range(dim[2]):    
                    temp = f.readline().rstrip('\n')
                    value = temp.split('"')[-2]
                    value_list.append(value)
                    if 'Secondary' not in title:
                        color[temp[1]] = float(value) if 'Hydrogen' not in ylabel else 0 if value == 'None' else 1
                    else:
                        color[temp[1]] = ss.index(value)
            #坐标值
            elif 'x-axis' in line:
                x.extend(line.split()[2:-1])
            elif 'y-axis' in line:
                y.extend(line.split()[2:-1])
            elif line[0] == '"' and line[dim[0]+1] == '"':
                temp = [color[line[j]] for j in range(1, dim[0]+1)]
                arr.append(temp)
            line = f.readline().rstrip('\n')
        #必须按行反向列表，因为xpm中的数据默认是反向的，即最后一行数据才是开始值
        arr.reverse()
    #处理一下维度，因为有的xpm文件坐标个数会大于下面的矩阵维度dim[0](如gmx sham)
    if len(x) > dim[0]:
        x.pop()
        y.pop()
    
    #绘图
    plt.figure(figsize=(8, 6))
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    X, Y = np.meshgrid(x, y)
    Z = np.array(arr, dtype = float)
    #氢键map图
    if "Hydrogen" in ylabel:
        h = plt.contourf(X, Y, Z, np.linspace(0, 1, 3), colors = ['white', 'red'])
        cb = plt.colorbar(h, orientation = 'horizontal', fraction=0.03)
        cb.set_ticks([0.25, 0.75])
        cb.set_ticklabels(['None', 'Present'])
    #蛋白二级结构图
    elif 'Secondary' in title:
        bar_label = []
        for i in ss:
            if i in value_list:
                bar_label.append(color_map[ss.index(i)])
        h = plt.contourf(X, Y, Z, np.linspace(0, len(color)-1, len(color)+1), colors = bar_label)
        cb = plt.colorbar(h, orientation = 'horizontal')
        cb.set_ticks(np.linspace(0, len(color)-1, len(color)+1)+0.5)
        cb.set_ticklabels(value_list)
    #其他类型的图
    else:
        h = plt.contourf(X, Y, Z, np.linspace(min(color.values()), max(color.values()), 9),cmap = "jet")
        cb = plt.colorbar(h)
    cb.ax.tick_params(labelsize=13)
    cb.set_label(legend, fontsize=18)
    
    plt.title(title, fontsize=18)
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=18)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim([np.min(x), np.max(x)])
    plt.ylim([np.min(y), np.max(y)])
    plt.savefig(fname.split('.')[0]+'.png', dpi=300)
#    plt.show()
    
def Help(argv):
    print('->>Description:\nThis program can read most common xpm file generated by gromacs tools, then plot figure')
    print('Usage:\n\t./%s  xxx.xpm\n' %(argv))
    exit(-1)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        Help(sys.argv[0])
    Read_Plot_XPM(sys.argv[1])
