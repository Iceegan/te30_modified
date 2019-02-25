import string;
import sys
import tesp_support.fncs as fncs
import tesp_support.simple_auction as simple_auction
if sys.platform != 'win32':
	import resource

time_stop = int(sys.argv[1])
time_granted = 0
count = 0

# requires yaml specificied in an envar
fncs.initialize()

#fncs.publish(sw_A_status, 'CLOSED')
#fncs.publish(sw_B_status, 'CLOSED')
#fncs.publish(sw_C_status, 'CLOSED')
while time_granted < time_stop:
	time_granted = fncs.time_request(time_stop)
	events = fncs.get_events()
	if (count == 100):
		print(events)
		print(time_granted, "Switching off AC in houses")
		fncs.publish('F1_House_B0/system_mode', 'OFF')
		fncs.publish('F1_House_C1/system_mode', 'OFF')
		fncs.publish('F1_House_C2/system_mode', 'OFF')
		fncs.publish('F1_House_B3/system_mode', 'OFF')
		fncs.publish('F1_House_B4/system_mode', 'OFF')
		fncs.publish('F1_House_A5/system_mode', 'OFF')
		fncs.publish('F1_House_B6/system_mode', 'OFF')
		fncs.publish('F1_House_B7/system_mode', 'OFF')
		fncs.publish('F1_House_A8/system_mode', 'OFF')
		fncs.publish('F1_House_A9/system_mode', 'OFF')
		fncs.publish('F1_House_C10/system_mode', 'OFF')
	if (count == 300):
		print(events)
		print(time_granted, "Switching off AC in houses")
		fncs.publish('F1_House_B0/system_mode', 'ON')
		fncs.publish('F1_House_C1/system_mode', 'ON')
		fncs.publish('F1_House_C2/system_mode', 'ON')
		fncs.publish('F1_House_B3/system_mode', 'ON')
		fncs.publish('F1_House_B4/system_mode', 'ON')
		fncs.publish('F1_House_A5/system_mode', 'ON')
		fncs.publish('F1_House_B6/system_mode', 'ON')
		fncs.publish('F1_House_B7/system_mode', 'ON')
		fncs.publish('F1_House_A8/system_mode', 'ON')
		fncs.publish('F1_House_A9/system_mode', 'ON')
		fncs.publish('F1_House_C10/system_mode', 'ON')
	count = count+1
	#print(count)
	for topic in events:
		value = fncs.get_value(topic)
		#print (time_granted, topic, value, flush=True)
		if topic == 'refload':
			if simple_auction.parse_fncs_magnitude(value) > 250000:
				print (time_granted, "Refload too large! Opening switch. Value = ",simple_auction.parse_fncs_magnitude(value), flush=True)
				fncs.publish('eplus_sw_status', 'OPEN')


fncs.finalize()

if sys.platform != 'win32':
	usage = resource.getrusage(resource.RUSAGE_SELF)
	RESOURCES = [
	('ru_utime', 'User time'),
	('ru_stime', 'System time'),
	('ru_maxrss', 'Max. Resident Set Size'),
	('ru_ixrss', 'Shared Memory Size'),
	('ru_idrss', 'Unshared Memory Size'),
	('ru_isrss', 'Stack Size'),
	('ru_inblock', 'Block inputs'),
	('ru_oublock', 'Block outputs')]
	print('Resource usage:')
	for name, desc in RESOURCES:
		print('  {:<25} ({:<10}) = {}'.format(desc, name, getattr(usage, name)))
