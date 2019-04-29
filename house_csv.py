#!/usr/bin/env python3
import json
import dask
import dask.bag as db
import dask.dataframe as dd
import csv
from collections import OrderedDict

# with open ('inverter_TE_Challenge_metrics.json') as json_file:
#     data = json.load(json_file)
#
#     for
#
# b = db.read_text("file://./inverter_TE_Challenge_metrics.json").map(json.loads)
# print(b)

#json_data = dd.read_json("./inverter_TE_Challenge_metrics.json", orient='columns').compute()
lp = open ("house_TE_Challenge_metrics.json").read()

json_data = json.loads(lp)
total_load_index = json_data['Metadata']['total_load_avg']['index']
json_data.pop('Metadata')
json_data.pop('StartTime')
#make this more generic below
obj_keys = list(json_data[list(json_data.keys())[0]].keys())
#sorted =  OrderedDict(sorted(json_data.items(), key=lambda item: socket.inet_aton(item[1])))
times = list(json_data.keys())
times.sort(key=float)
print(times)

for obj in obj_keys:
    filename = './profiles/' + obj + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        outwriter = csv.writer(csvfile, delimiter=',')
        outwriter.writerow(['startTime','endTime','energy'])
        for time in times:
            time = str(time)
        for timestamp in times:
            if(obj in json_data[timestamp]):
                interval = str(int(timestamp)/900).split('.')[0]
                outwriter.writerow([interval, interval, (-json_data[timestamp][obj][total_load_index])])
