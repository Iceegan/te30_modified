import string;
import json
import sys
import tesp_support.fncs as fncs
import tesp_support.simple_auction as simple_auction
if sys.platform != 'win32':
	import resource

time_stop = int(sys.argv[1])
time_granted = 0

fncs.initialize()

while time_granted < time_stop:
	#time_granted = fncs.time_request(time_stop)
	time_granted = fncs.time_request(time_stop)
	events = fncs.get_events()
	print(time_granted, events)
	for topic in events:
		value = fncs.get_value(topic)
		#print()
		#can improve this by creating a set of all the relevant topics
		#Check if topic is in the set
		#if ('batt_charge' in topic):
			#print('Charge topic')
		#	batt_num = topic[0:4]
		#	if simple_auction.parse_fncs_number(value) > 0.95:
				#print('inside charge topic')
				#print(batt_num, '_batt_P_Out')
		#		fncs.publish(batt_num + '_batt_P_Out', 1000)

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
