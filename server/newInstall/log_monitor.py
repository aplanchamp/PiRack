import time
import subprocess
import os
from time import sleep
from newInstall import global_settings
from newInstall import Rasp
from newInstall import Stack
import csv
from configparser import ConfigParser
from newInstall import stack_power
import sh

global_settings.init()
syslog_file = open('/var/log/syslog','r')

# instantiate
configRack = ConfigParser()

# parse existing file
configRack.read('structure_rack.ini')

def log_monitor():

	syslog_file.seek(0,2) # Go to end of file
	while True:
		line = syslog_file.readline()
		if not line:
			sleep(0.1);
			continue
		yield line

#monitor function
print('---------------------------------------')
print('---- Starting monitoring syslog... ----')
print('---------------------------------------')
generateur = log_monitor()

def detect_dhcprequest():
	time_start=time.time()
	timeout=40
	limit_detected = global_settings.ip + int(configRack['rack']['pi_stack'])
	print('----------------------------------------------')
	print('---- Detection of machines in progress... ----')
	print('----------------------------------------------')
	#pi_stacks = int(configRack['rack']['pi_stack'])
	for i in generateur:
		if (time.time() < time_start+timeout) and (global_settings.ip<limit_detected):
			res=i.find( 'DHCPREQUEST',0 )
			if(res != -1): #String DHCPREQUEST FOUND
				print('**** Log detected: '+i) # Print line
				index_from = i.find('from',0) #looking for 'from' string
				if(index_from!= -1): # If from found
					mac=i[index_from+5:index_from+5+17]
					if mac in global_settings.dict_rasps:
						print('**** '+mac+' Already added in dict_rasps ****')
					else:
						global_settings.dict_rasps[mac] = Rasp.Rasp()
						global_settings.dict_rasps[mac]._mac = mac
						global_settings.dict_rasps[mac]._ip = '192.168.23.'+str(global_settings.ip) # Add dict_mac[mac@]=IP
						global_settings.ip = global_settings.ip + 1 # Increment IP
						global_settings.dict_rasps[mac]._stack = global_settings.stack
						for key in global_settings.dict_rasps:
							#print (global_settings.dict_rasps[key])
							print('**** ' +key)
		else:
			global_settings.stack = global_settings.stack+1
			return

def write_dhcpd_mac():
	host_number=1 # Number for dhcpd.conf only, this is not the ID of the Rasp
	#Create dhcpd.conf addressing dynamically addresses to Pi from 192.168.23.100-150
	dhcpd_conf_m = open("dhcpd_m.conf",'w')
	dhcpd_conf_m.write
	dhcpd_conf_m.write('option domain-name "example.org";\noption domain-name-servers ns1.example.org, ns2.example.org;\nauthoritative;\n')
	dhcpd_conf_m.write('default-lease-time 75;\nmax-lease-time 75;\n')
	dhcpd_conf_m.write('log-facility local7;\n')
	#dhcpd_conf_m.write('\nsubnet 192.168.23.0 netmask 255.255.255.0 {\nrange 192.168.23.10 192.168.23.150;\noption routers 192.168.21.254;\noption broadcast-address 192.168.23.255;\ndefault-lease-time 75;\n}')#2.5 minutes\nmax-lease-time 75; #2.5minutes max\n\n')
	dhcpd_conf_m.write('\nsubnet 192.168.23.0 netmask 255.255.255.0 {\noption subnet-mask 255.255.255.0;\noption broadcast-address 192.168.23.255;\noption routers 192.168.23.1;\npool {\nrange 192.168.23.10 192.168.23.150;\n}\n}\n')
	for key in global_settings.dict_rasps:
		dhcpd_conf_m.write('\nhost rasp'+str(host_number)+'{\n')
		dhcpd_conf_m.write('hardware ethernet '+global_settings.dict_rasps[key]._mac+';\n')
		dhcpd_conf_m.write('fixed-address '+global_settings.dict_rasps[key]._ip+';\n')
		host_number = host_number +1
		dhcpd_conf_m.write('max-lease-time 75;\n}')
	os.system('sudo mv dhcpd_m.conf /etc/dhcp/dhcpd.conf') #Replacing the dhcpd.conf file

def restart_dhcp():
	os.system('sudo /etc/init.d/isc-dhcp-server restart')

#scp and ssh to an distant Pi
def scp_to_pi(filepath, Pi_ip, remote_path):
        #Send file to a specific Pi IP
        subprocess.call( ['scp', filepath, "@".join(['root',":".join([Pi_ip,remote_path])]) ])
        print("file ")
        print(filepath)
        print("sent to ")
        print(Pi_ip)
        return

def dict_rasps_csv():
	file = open(global_settings.dict_rasps_csv,'w')
	id=1
	for k in global_settings.dict_rasps:
		try:
			file.write(str(id)+","+global_settings.dict_rasps[k]._mac+","+str(global_settings.dict_rasps[k]._stack)+","+global_settings.dict_rasps[k]._ip+"\n")
			id = id+1
		except:
			print("Do not succeed in writtin the CSV file dict_rasps.csv")
	print('-------------------------------------------')
	print("**** Generation of dict_rasps.csv file ****")
	print('-------------------------------------------')

def dict_stacks_csv():
        file = open(global_settings.dict_stacks_csv,'w')
        for k in global_settings.stacks:
                try:
                        file.write(str(global_settings.stacks[k]._id)+","+global_settings.stacks[k]._power+","+global_settings.stacks[k]._Sstatus+","+str(global_settings.stacks[k]._x)+","+str(global_settings.stacks[k]._y)+"\n")
              
                except:
                        print("Do not succeed in writtin the CSV file dict_stacks.csv")
        print('--------------------------------------------')
        print("**** Generation of dict_stacks.csv file ****")
        print('--------------------------------------------')


def install():
	print("---------------------------")
	print("**** Installation ****")
	print("**** Powering Off stacks...")
	print("---------------------------")
	nbr_stacks = int(configRack['rack']['nbr_stack'])
	p = nbr_stacks
	while (p>0):
		stack_power.powerdown_stack(p)
		p=p-1
	sleep(1)
	while global_settings.stack < nbr_stacks + 1 :
		stack_num= str(global_settings.stack)
		print('--------------------------------------------')
		print('---- Firing ON stack number: ' +str(global_settings.stack)+' ----')
		print('--------------------------------------------')
		stack_power.powerup_stack(global_settings.stack)
		global_settings.stacks[global_settings.stack]=Stack.Stack()
		global_settings.stacks[global_settings.stack]._id=global_settings.stack
		global_settings.stacks[global_settings.stack]._power="On"
		global_settings.stacks[global_settings.stack]._x=configRack[stack_num]['x']
		global_settings.stacks[global_settings.stack]._y=configRack[stack_num]['y']
		# Detect mac addresses for 60s
		detect_dhcprequest()
		print('-------------------------------------')
		print('---- Powering OFF stack '+str(global_settings.stack-1)+' ----')
		print('-------------------------------------')
		stack_power.powerdown_stack(global_settings.stack-1)
		#global_settings.stacks[global_settings.stack-1]._power="Off"
		print('-------------------------------------------------------------')
		print('---- Exporting temporary DHCPD.CONF with stacks detected ----')
		print('-------------------------------------------------------------')
		write_dhcpd_mac()
		restart_dhcp()
	dict_rasps_csv()
	print('--------------------------------')
	print("---- Powering On the PiRack ----")
	print('--------------------------------')
	p = nbr_stacks
	while(p>0):
		stack_power.powerup_stack(p)
		#global_settings.stacks[p]._power="On"
		p = p-1
	print('---------------------------------------')
	print("---- Getting fixed IP addresses... ----")
	print('---------------------------------------')
	sleep(25)
	k=nbr_stacks
	while(k>0):
		ping_rasps_in_stack(k)
		print(global_settings.stacks[k])
		k=k-1
	#get_rasps_from_csv()
	dict_stacks_csv()
	for k in global_settings.dict_rasps:
		#scp_to_pi('./configuration.ini',global_settings.rasps[k]._ip,'/home/pi/Documents/Project_proto/slave_server/')
		os.system('bash ./slave/deploy_slave.sh ' + global_settings.dict_rasps[k]._ip)
		#subprocess.call( ['ssh', "@".join(['root',global_settings.rasps[k]._ip] ) ,'sudo bash', '/home/pi/Documents/Project_proto/slave_server/slave' ])		
	print('-----------------------------------')
	print('**** End of Installation phase ****')
	print('-----------------------------------')

def get_rasps_from_csv():
	global_settings.rasps={}
	print("-----------------------------------------------------------")
	print("Generating the global variable dict_rasps_csv from the csv file")
	print("-----------------------------------------------------------")
		
	try:
		with open(global_settings.dict_rasps_csv,'r') as ofile:
			mcsv = csv.reader(ofile, delimiter=',' )
			for row in mcsv:
				print(row[0])
				global_settings.rasps[row[0]] = Rasp.Rasp()
				global_settings.rasps[row[0]]._id = row[0]
				global_settings.rasps[row[0]]._mac = row[1]
				global_settings.rasps[row[0]]._ip = row[3]
				global_settings.rasps[row[0]]._stack = row[2]
				global_settings.rasps[row[0]]._power = 'On'
				global_settings.rasps[row[0]]._cpu = '--'
				global_settings.rasps[row[0]]._temperature = '--'
				global_settings.rasps[row[0]]._Lping = '--'
				try:
					#bash ping command from master to pis
					sh.ping(row[3], "-c 2",_out="/dev/null")
					print("ping to ",row[3] ," OK")
					global_settings.rasps[row[0]]._Rstatus = 'okStatus'
				except sh.ErrorReturnCode_1:
					print("no response from", row[3])
					global_settings.rasps[row[0]]._Rstatus = 'koStatus'
				print(global_settings.rasps[row[0]]._id+' '+global_settings.rasps[row[0]]._ip + ' ' + global_settings.rasps[row[0]]._mac+' '+global_settings.rasps[row[0]]._stack)
			print(" Rasps generated from csv file\n")
	except:
		print("Installation needed")

def get_stacks_from_csv():
        global_settings.stacks={}
        print("----------------------------------------------------------------")
        print("Generating the global variable dict_stacks_csv from the csv file")
        print("----------------------------------------------------------------")

        try:
                with open(global_settings.dict_stacks_csv,'r') as ofile:
                        mcsv = csv.reader(ofile, delimiter=',' )
                        for row in mcsv:
                                global_settings.stacks[row[0]] = Stack.Stack()
                                global_settings.stacks[row[0]]._id = row[0]
                                global_settings.stacks[row[0]]._power = row[1]
                                global_settings.stacks[row[0]]._Sstatus = row[2]
                                global_settings.stacks[row[0]]._x = row[3]
                                global_settings.stacks[row[0]]._y = row[4]
                                #print(global_settings.rasps[row[0]]._id+' '+global_settings.rasps[row[0]]._ip + ' ' + global_settings.rasps[row$
                        print(" Stacks generated from csv file\n")
        except:
                 print("Installation needed")
           
def ping_rasps_in_stack(nstack):
	print('------------------------------------')
	print("---- Ping command in process... ----")
	print('------------------------------------')
	tmp = 0
	for key in global_settings.dict_rasps:
		if global_settings.dict_rasps[key]._stack == nstack:
			ip = global_settings.dict_rasps[key]._ip
			try:
				#bash ping command from master to pis
				sh.ping(ip, "-c 2",_out="/dev/null")
				tmp = tmp + 1
			except sh.ErrorReturnCode_1:
				print("no response from", ip)
				
	if tmp == 0:
		global_settings.stacks[nstack]._Sstatus = "koStatus"
	else:
		if tmp< int(configRack['rack']['pi_stack']):
			global_settings.stacks[nstack]._Sstatus = "warningStatus"
		else:
			global_settings.stacks[nstack]._Sstatus = "okStatus"
	return


