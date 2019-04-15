house_num = ['b1m1','b1m2','b1m3','b1m4','b1m5','b1m6','b1m7','b1m8','b1m9','b1m10','b2m1','b2m2','b2m3','b2m4','b2m5','b2m6','b2m7','b2m8','b2m9','b2m10','b3m1','b3m2','b3m3','b3m4','b3m5','b3m6','b3m7','b3m8','b3m9','b3m10']
phases = ['BS','CS','CS','BS','BS','AS','BS','BS','AS','AS','CS','AS','AS','AS','CS','AS','AS','CS','CS','BS','BS','CS','BS','BS','BS','AS','AS','CS','AS','CS']
line_name = ['branch_1_line_1','branch_1_line_2','branch_1_line_3','branch_1_line_4','branch_1_line_5','branch_1_line_6','branch_1_line_7','branch_1_line_8','branch_1_line_9','branch_1_line_10', \
'branch_2_line_1','branch_2_line_2','branch_2_line_3','branch_2_line_4','branch_2_line_5','branch_2_line_6','branch_2_line_7','branch_2_line_8','branch_2_line_9','branch_2_line_10', \
'branch_3_line_1','branch_3_line_2','branch_3_line_3','branch_3_line_4','branch_3_line_5','branch_3_line_6','branch_3_line_7','branch_3_line_8','branch_3_line_9','branch_3_line_10',]

meter_name = ['branch_1_meter_1','branch_1_meter_2','branch_1_meter_3','branch_1_meter_4','branch_1_meter_5','branch_1_meter_6','branch_1_meter_7','branch_1_meter_8','branch_1_meter_9','branch_1_meter_10', \
'branch_2_meter_1','branch_2_meter_2','branch_2_meter_3','branch_2_meter_4','branch_2_meter_5','branch_2_meter_6','branch_2_meter_7','branch_2_meter_8','branch_2_meter_9','branch_2_meter_10', \
'branch_3_meter_1','branch_3_meter_2','branch_3_meter_3','branch_3_meter_4','branch_3_meter_5','branch_3_meter_6','branch_3_meter_7','branch_3_meter_8','branch_3_meter_9','branch_3_meter_10',]


ofile = open("lines.txt",'w')
for i in range(1,30):
    ostring ="""subscribe "precommit:batt_inv_F1_house_B0.P_Out <- testAgent/batt_0_P_Out";""".format(meter_name[i-1], line_name[i], meter_name[i]);
    ofile.write(ostring)

ofile.close()
