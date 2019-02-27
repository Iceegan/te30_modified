import string;
import json
import sys
import tesp_support.fncs as fncs
import tesp_support.simple_auction as simple_auction
if sys.platform != 'win32':
	import resource

MAX_HVAC_TEMP = 85.0
MAX_LOAD = 400000

time_stop = int(sys.argv[1])
time_granted = 0
firstLoop = True


#establish list of hvac controllers for hvac monitoring
dict_file = open("TE_Challenge_glm_dict.json").read()
glm_dict = json.loads(dict_file)
house_list = list(glm_dict['houses'].keys()) #need to add #

fncs.initialize()

while time_granted < time_stop:
	time_granted = fncs.time_request(time_stop)
	#Default to on
	if firstLoop:
		firstLoop = False
		for house in house_list:
			fncs.publish(house + '_hvac/system_mode', 'ON')
			print(house + '/system_mode set ON', flush = True)
	events = fncs.get_events()
	for topic in events:
		value = fncs.get_value(topic)
		if topic == 'refload' and simple_auction.parse_fncs_magnitude(value) > MAX_LOAD:
			for house in house_list:
				fncs.publish(house + '_hvac/system_mode', 'OFF')
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
