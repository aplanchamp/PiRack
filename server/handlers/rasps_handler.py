# T3 - S9 Projects
# Description: This file manage rasp objects

from newInstall import global_settings
import csv
import json
from newInstall import Rasp
from newInstall import log_monitor

global_settings.init()

PORT = 1026

def obj_to_json(rasp):
	_id = rasp._id
	_ip = rasp._ip
	_mac = rasp._mac
	_power = rasp._power
	_cpu = rasp._cpu
	_stack = rasp._stack
	_Lping = rasp._Lping
	_temperature = rasp._temperature
	_Rstatus = rasp._Rstatus
	raspObject = json.JSONEncoder().encode({
		"id": _id,
		"ip": _ip,
		"mac": _mac,
		"power": _power,
		"cpu": _cpu,
		"stack": _stack,
		"Rstatus":_Rstatus,
		"Lping":_Lping,
		"temperature":_temperature
		})
	return raspObject


def get_rasp_by_id(rrid):
	rid = str(rrid)
	rasp = {}
	try:
		rasp = global_settings.rasps[rid]
		return obj_to_json(rasp) 
	except:
		return rasp
 
def update_rasp_by_id(rrid,attribute,data,status):
	rid = str(rrid)
	if attribute=='ping':
		if status==200:
			global_settings.rasps[rid]._Lping=data
			global_settings.rasps[rid]._Rstatus="okStatus"
		else:
			global_settings.rasps[rid]._Rstatus="koStatus"
	elif attribute=='shutdown' and status==200:
		response = os.system( 'ping -c 1 -w2'+ IP + "> /dev/null 2>&1")
		if response != 0:
			global_settings.rasps[rid]._power="Off"
	elif attribute=='cpu' and status==200:
		global_settings.rasps[rid]._cpu = data
	elif attribute=='temperature' and status==200:
		global_settings.rasps[rid]._temperature=data
	return


def get_rasps():
	rasps = [obj_to_json(global_settings.rasps[key]) for key in global_settings.rasps]
	return rasps
	
#
# def get_list_ip():
#         list_ip = []
#         mcsv = csv.reader(open(global_settings.reachable_rasps_csv,'rb'))
#
#         for row in mcsv:
#                 list_ip.append(row[1])
#         return list_ip
#
# def get_list_hostname():
#         list_hostname = []
#         mcsv = csv.reader(open(global_settings.reachable_rasps_csv,'rb'))
#         for row in mcsv:
#                 list_hostname.append(row[2])
#         return list_hostname
#
# def add_new_rasps_to_dict(nstack):
#         print("-----------------------------------------------------------")
#         print("Add into the dict_rasps dictionnary new Rasps object ")
#         print("according their mac address")
#         # If already added, do nothing
#         # To use just after creating the csv file
#         print("-----------------------------------------------------------")
#
#         mcsv = csv.reader(open(global_settings.reachable_rasps_csv,'r'))
#         for row in mcsv:
#                 if row[0] in global_settings.dict_rasps:
#                         print(" /!\ "+row[0]+" already is in dictionnary in stack number "+ str(global_settings.dict_rasps[row[0]]._stack))
#                         print(" /!\ You can delete existing item using .delete_rasp('"+row[0]+"')\n")
#                 else:
#                         # Attribution des mac, ip et hostname de l'objet
#                         global_settings.dict_rasps[row[0]] = Rasp.Rasp(row[0])
#                         global_settings.dict_rasps[row[0]]._ip = row[1]
#                         global_settings.dict_rasps[row[0]]._hostname = row[2]
#                         global_settings.dict_rasps[row[0]]._stack = nstack
#                         print(global_settings.dict_rasps[row[0]]._mac+' '+global_settings.dict_rasps[row[0]]._ip + ' ' + global_settings.dict_rasps[row[0]]._hostname + ' ' + str(global_settings.dict_rasps[row[0]]._stack))
#                         print(" added in dictionnary\n")
#         dict_rasps_csv()
#         return global_settings.dict_rasps
#
# def delete_rasp(mac):
#         # Delete from dictionnary a Pi by its Mac @
#         global_settings.dict_rasps.pop(mac, None)
#         print("Raspberry " + mac + " has been deleted")
#         return
#
# def dict_rasps_csv():
#         with open(global_settings.dict_rasps_csv,'w') as ofile:
#                 writer = csv.writer(ofile, delimiter=',' )
#                 for key in global_settings.dict_rasps:
#                         writer.writerow( [key, global_settings.dict_rasps[key]._ip, global_settings.dict_rasps[key]._hostname, global_settings.dict_rasps[key]._stack, global_settings.dict_rasps[key]._level] )
#                 print("** export csv success")
#         return
