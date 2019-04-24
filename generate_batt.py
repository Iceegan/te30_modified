house_num = ['b1m1','b1m2','b1m3','b1m4','b1m5','b1m6','b1m7','b1m8','b1m9','b1m10','b2m1','b2m2','b2m3','b2m4','b2m5','b2m6','b2m7','b2m8','b2m9','b2m10','b3m1','b3m2','b3m3','b3m4','b3m5','b3m6','b3m7','b3m8','b3m9','b3m10']
phases = ['BS','CS','CS','BS','BS','AS','BS','BS','AS','AS','CS','AS','AS','AS','CS','AS','AS','CS','CS','BS','BS','CS','BS','BS','BS','AS','AS','CS','AS','CS']
meter_name = ['branch_1_meter_1','branch_1_meter_2','branch_1_meter_3','branch_1_meter_4','branch_1_meter_5','branch_1_meter_6','branch_1_meter_7','branch_1_meter_8','branch_1_meter_9','branch_1_meter_10', \
'branch_2_meter_1','branch_2_meter_2','branch_2_meter_3','branch_2_meter_4','branch_2_meter_5','branch_2_meter_6','branch_2_meter_7','branch_2_meter_8','branch_2_meter_9','branch_2_meter_10', \
'branch_3_meter_1','branch_3_meter_2','branch_3_meter_3','branch_3_meter_4','branch_3_meter_5','branch_3_meter_6','branch_3_meter_7','branch_3_meter_8','branch_3_meter_9','branch_3_meter_10',]

ofile = open("inverters.txt",'w')
for i in range(30):
    ostring ="""//{2}
object transformer {{
     name {1}_house_trans;
     phases {0};
     from {2};
     to {1}_house_node;
     configuration house_transformer;
}}

object triplex_node {{
  name {1}_house_node;
  phases {0};
  nominal_voltage 120;
}}

object triplex_line {{
	groupid F1_Triplex_Line;
	phases {0};
	from {1}_house_node;
	to {1}_batt_meter;
	length 10 ft;
	configuration TLCFG;
}}

object triplex_line {{
	groupid F1_Triplex_Line;
	phases {0};
	from {1}_house_node;
	to {1}_solar_meter;
	length 10 ft;
	configuration TLCFG;
}}

object triplex_meter {{
  name {1}_solar_meter;
	phases {0};
	nominal_voltage 120;
	groupid inverter_meter;

	object inverter {{
		name {1}_solar_inv;
		phases {0};
		inverter_type FOUR_QUADRANT;
		power_factor 1;
		use_multipoint_efficiency TRUE;
		inverter_manufacturer XANTREX;
		maximum_dc_power 6500;
		four_quadrant_control_mode CONSTANT_PF;
		generator_status ONLINE;
		rated_power 6500;
		inverter_efficiency 0.90;

		object solar {{
			name {1}_solar;
			generator_mode SUPPLY_DRIVEN;
			generator_status ONLINE;
			panel_type SINGLE_CRYSTAL_SILICON;
			orientation FIXED_AXIS;
			rated_power 7500;
		}};
    object metrics_collector {{
    	interval 300;
    }};
	}};
}}

object triplex_meter {{
  name {1}_batt_meter;
	phases {0};
	nominal_voltage 120;
	groupid inverter_meter;

	object inverter {{
		name {1}_batt_inv;
		phases {0};
		inverter_type FOUR_QUADRANT;
		power_factor 1;
		use_multipoint_efficiency TRUE;
		inverter_manufacturer XANTREX;
		//maximum_dc_power 10000; //Might need to less than rated_power for the battery
		four_quadrant_control_mode CONSTANT_PQ;
		generator_status ONLINE;
		rated_power 6500;
		//rated_battery_power 10000;
		inverter_efficiency 0.90;
		P_Out -700; //VA

		object battery {{
			name {1}_batt;
			parent {1}_batt_inv;
			use_internal_battery_model TRUE;
			battery_type LI_ION;
			rated_power 10000;
			nominal_voltage 120;
			battery_capacity 14 kWh;
			round_trip_efficiency 0.9;
			state_of_charge 0;
			generator_mode SUPPLY_DRIVEN;
		}};
    object metrics_collector {{
    	interval 300;
    }};
	}};
}}\n\n""".format(phases[i], house_num[i], meter_name[i]);
    ofile.write(ostring)

ofile.close()
