def init():

	# Dictionnary of Pis available in the network
	global rasps_object
	rasps_object = {}

	global dict_rasps
	dict_rasps = {}

	global rasps
	rasps = {}
	
	global stacks
	stacks = {}

	global stack
	stack=1	

	global id
	id=20
	
	global ip
	ip = 70

	global reachable_rasps_csv
	reachable_rasps_csv = 'reachable_rasps.csv'

	global rasp_mac_network
	rasp_mac_network = 'rasp_mac_network.csv'

	global led0_script_name
	led0_script_name = 'script_led0.sh'

	global dict_rasps_csv
	dict_rasps_csv = 'dict_rasps.csv'
	
	global dict_stacks_csv
	dict_stacks_csv = 'dict_stacks.csv'

	global path_to_leases
	path_to_leases = '/var/lib/dhcp/dhcpd.leases'
