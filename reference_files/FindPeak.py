from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = open('raman file/raman data.csv','r', encoding='unicode_escape')
lines = file.readlines()
file.close()

xposition = 0
yposition = 3

xlist = []
ylist = []
flist = []

# info = lines[0].split(',')
lines.remove(lines[0])
ycheck = []
for d in lines:
    datas = d.split(',')
    ycheck.append(float(datas[yposition]))

for l in lines:
    data = l.split(',')
    xlist.append(str(float(data[xposition])))
    ylist.append(str(float(data[yposition])))
    flist.append(str((max(ycheck)-float(data[yposition]))))

out = open('raman file/temp.csv','w')
xline = ','.join(xlist)+'\n'
yline = ','.join(ylist)+'\n'
fline = ','.join(flist)
out.write(xline)
out.write(yline)
out.write(fline)
out.close()

data = pd.read_csv('raman file/temp.csv', header=None)
print(data)
# for m in range(data.shape[0]):
data1 = data.iloc[0, :-1]
data2 = data.iloc[1, :-1]
data3 = data.iloc[2, :-1]
ave = (sum(data3)/len(data3))*1.15
# peaks, _ = find_peaks(data3, height=10)  # peaks:峰所在的位置 data[peaks]：峰对应的值
# print(peaks)
# 寻峰作图
# data_n = np.array(data1)
# valleys = argrelextrema(data_n, comparator=np.less_equal, order=5)
# print(valleys[0])
# for i in range(len(valleys[0])):
#     plt.annotate(valleys[0][i], xy=(valleys[0][i], data_n[valleys[0][i]]), xytext=(valleys[0][i], data_n[valleys[0][i]] + 10-i),
#                  arrowprops=dict(arrowstyle='->'))
# plt.plot(data)
# plt.plot(peaks, data[peaks], "|")
# plt.show()
# 寻谷作图

data_nx = np.array(data1)
data_ny = np.array(data2)
data_n = np.array(data3)
valleys = argrelextrema(data_n, comparator=np.less_equal, order=5)

# for i in range(len(valleys[0])):
#     plt.annotate(valleys[0][i], xy=(valleys[0][i], data_n[valleys[0][i]]), xytext=(valleys[0][i], data_n[valleys[0][i]] + 10-i),
#                  arrowprops=dict(arrowstyle='->'))

data_v = list(data_n[valleys])
data_xv = list(data_nx[valleys])
data_yv = list(data_ny[valleys])

valleys_p = []
data_p = []

for n in data_v:
    if n < ave:
        pos = data_v.index(n)
        valleys_p.append(data_xv[pos])
        data_p.append(data_yv[pos])


plt.plot(data_nx, data_ny)
i = 0
while i < len(valleys_p):
    plt.plot([valleys_p[i],valleys_p[i]], [1000, data_p[i]], color='b')
    i += 1
plt.xlabel('Raman Shift')
plt.ylabel('Counts (a.u.)')
plt.show()
print(valleys_p)