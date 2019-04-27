import json;
import sys;
import numpy as np;
import matplotlib as mpl;
import matplotlib.pyplot as plt;

nameroot = "TE_Challenge"
lp = open ("TE_Challenge_glm_dict.json").read()
"""
dict = json.loads(lp)
sub_keys = list(dict['feeders'].keys())
sub_keys.sort()
inv_keys = list(dict['inverters'].keys())
inv_keys.sort()
hse_keys = list(dict['houses'].keys())
hse_keys.sort()
mtr_keys = list(dict['billingmeters'].keys())
mtr_keys.sort()
xfMVA = dict['transformer_MVA']
matBus = dict['matpower_id']
print ("\n\nFile", nameroot, "has substation", sub_keys[0], "at Matpower bus", matBus, "with", xfMVA, "MVA transformer")
print("\nFeeder Dictionary:")
for key in sub_keys:
    row = dict['feeders'][key]
    print (key, "has", row['house_count'], "houses and", row['inverter_count'], "inverters")
print("\nBilling Meter Dictionary:")
for key in mtr_keys:
    row = dict['billingmeters'][key]
    print (key, "on phase", row['phases'], "of", row['feeder_id'], "with", row['children'])
print("\nHouse Dictionary:")
for key in hse_keys:
    row = dict['houses'][key]
    print (key, "on", row['billingmeter_id'], "has", row['sqft'], "sqft", row['cooling'], "cooling", row['heating'], "heating", row['wh_gallons'], "gal WH")
    # row['feeder_id'] is also available
print("\nInverter Dictionary:")
for key in inv_keys:
    row = dict['inverters'][key]
    print (key, "on", row['billingmeter_id'], "has", row['rated_W'], "W", row['resource'], "resource")
    # row['feeder_id'] is also available
"""
# parse the substation metrics file first; there should just be one entity per time sample
# each metrics file should have matching time points
lp_s = open ("substation_TE_Challenge_metrics.json").read()
lst_s = json.loads(lp_s)
print ("\nMetrics data starting", lst_s['StartTime'])

# make a sorted list of the sample times in hours
lst_s.pop('StartTime')
meta_s = lst_s.pop('Metadata')
times = list(map(int,list(lst_s.keys())))
times.sort()
print ("There are", len (times), "sample times at", times[1] - times[0], "second intervals")
hrs = np.array(times, dtype=np.float)
denom = 3600.0
hrs /= denom

time_key = str(times[0])

# parse the substation metadata for 2 things of specific interest
print ("\nSubstation Metadata for", len(lst_s[time_key]), "objects")
for key, val in meta_s.items():
    print (key, val['index'], val['units'])
    if key == 'real_power_avg':
        SUB_POWER_IDX = val['index']
        SUB_POWER_UNITS = val['units']
    elif key == 'real_power_losses_avg':
        SUB_LOSSES_IDX = val['index']
        SUB_LOSSES_UNITS = val['units']

# create a NumPy array of all metrics for the substation
sub_keys = ['network_node']
data_s = np.empty(shape=(len(sub_keys), len(times), len(lst_s[time_key][sub_keys[0]])), dtype=np.float)
print ("\nConstructed", data_s.shape, "NumPy array for Substations")
j = 0
for key in sub_keys:
    i = 0
    for t in times:
        ary = lst_s[str(t)][sub_keys[j]]
        data_s[j, i,:] = ary
        i = i + 1
    j = j + 1

# display a plot
fig, ax = plt.subplots(1, 1, sharex = 'col')

ax.plot(hrs, data_s[0,:,SUB_POWER_IDX], color="blue", label="Total")
#ax.plot(hrs, data_s[0,:,SUB_LOSSES_IDX], color="red", label="Losses")
ax.set_ylabel(SUB_POWER_UNITS)
ax.set_xlabel("Hour")
ax.set_title ("Substation Real Power at " + sub_keys[0])
ax.legend(loc='best')

plt.show()
