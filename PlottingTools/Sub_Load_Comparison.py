import pandas
import numpy as np
import csv
import matplotlib.pyplot as plt
import tikzplotlib
import sys
from pathlib import Path

mFile0 = Path(sys.argv[1] + "/power_output.csv")
mFile1 = Path(sys.argv[2] + "/power_output.csv")

def strToComp(str):
    #print(type(row[1][1]))
    if str[0]=='+':
        return float(complex(str[1:]).real)
    else:
        return float(complex(str).real)

def getAvgLoad(file, avgInt):
    arr = pandas.read_csv(file, skiprows=7)
    outSeries = arr[['# timestamp','network_node:distribution_load']]
    outSeries['network_node:distribution_load'] = outSeries['network_node:distribution_load'].map(strToComp)
    return outSeries.groupby(np.arange(len(outSeries))//avgInt).mean()

# outSeries.resample('15m').mean()
avg0 = getAvgLoad(mFile0,15)/1000
avg1 = getAvgLoad(mFile1,15)/1000
# avg1.rename('After')
# arr = pandas.read_csv(mFile0, skiprows=7)
avgFrame = pandas.concat([avg0, avg1], axis = 1)
avgFrame.columns = ['Traditional', 'With Transax']
print(avgFrame)


ax = avgFrame.plot(y=['Traditional', 'With Transax'], sharey=True)
ax.set_xlabel('Number of Elapsed 15 Minute Intervals')
ax.set_ylabel('Real Power Load (kW)')
# plt.show()

tikzplotlib.save("mytikz.tex")
