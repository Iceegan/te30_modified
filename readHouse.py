import json

lp_h = open('house_TE_Challenge_metrics.json').read()
lst_h = json.loads(lp_h)
#meta_h = lst_h['Metadata']
#print(meta_h)
target = lst_h['1515']
print(lst_h)
