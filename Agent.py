import string;
import json
import sys
import zmq
import fncs
import time

if sys.platform != 'win32':
	import resource


RIAPS = True 

time_stop = int(sys.argv[1])
time_granted = 0

fncs.initialize()


if(RIAPS):
	context = zmq.Context(1)
	server = context.socket(zmq.REP)
	server.bind("tcp://*:5555")


	batt_charges = {}
	solar_power = {}

	while time_granted < time_stop:
		events = fncs.get_events()
		for topic in events:
			value = fncs.get_value(topic)
			#Collect Most recent charge data
			if('batt_charge' in topic):
				batt_charges[topic] = value
			if('solar_power' in topic):
				solar_power[topic] = value
		if('step' in events):
			request = ''
			while(request != 'step'):
				msg = server.recv_pyobj()
				request = msg['request']
				if (request == 'postTrade'):
					print(request, time_granted, flush=True)
					req_batt_num = msg['ID']
					first = req_batt_num[0:1]
					second = req_batt_num[1:3]
					if (second[0] == '0'):
						second = second[1]
					m_batt_num = 'b' + first + 'm' + second
					keyname = m_batt_num + '_solar_power'
					if(keyname in solar_power):
						#Solar power is now positive in GridLabD
						batt_out = msg['power'] - float(solar_power[keyname].split(' ')[0])
						print('msg[\'power\']: ', str(msg['power']),flush=True)
						print('solar power:', str(float(solar_power[keyname].split(' ')[0])),flush=True)
						print('batt_out:', str(batt_out),flush=True)
					else:
						batt_out = 0
					fncs.publish(m_batt_num + '_batt_P_Out', str(batt_out))
					print('fncs published:', m_batt_num + '_batt_P_Out', str(batt_out))
					server.send_pyobj('Trade Posted')
				if (request == 'charge'):
					print(request, time_granted, flush=True)
					req_batt_num = msg['ID']
					first = req_batt_num[0:1]
					second = req_batt_num[1:3]
					if (second[0] == '0'):
						second = second[1]
					m_batt_num = 'b' + first + 'm' + second
					keyname = m_batt_num + '_batt_charge'
					if(keyname in batt_charges):
						charge = batt_charges[keyname]
					else:
						charge = '+0 pu'
					server.send_pyobj(charge)
			print(request, time_granted, flush=True)
			time_granted = fncs.time_request(time_stop)
			server.send_pyobj('Step Granted')
		else:
			time_granted = fncs.time_request(time_stop)
			print("Simulation Continue, new time_granted:", str(time_granted))
else:
	while time_granted < time_stop:
		time_granted = fncs.time_request(time_stop)



print('End of Simulation', flush=True)

server.close()
context.term()
print('zmq Closed', flush=True)
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
