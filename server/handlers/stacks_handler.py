# T3 - S9 Projects
# Description: This file manage rasp objects
import sh
import datetime
from newInstall import global_settings
import csv
import json
from newInstall import Rasp
from newInstall import log_monitor
from handlers import rasps_handler
from configparser import ConfigParser
global_settings.init()

# instantiate
configRack = ConfigParser()

# parse existing file
configRack.read('structure_rack.ini')

def get_rasps_from_stack(id):
	rid = []
	for key in global_settings.rasps:
		stack = int(global_settings.rasps[key]._stack)
		if stack == id:
			rid.append(int(global_settings.rasps[key]._id))
	return rid

def obj_to_json(stack):
	_id = stack._id
	_power = stack._power
	_Sstatus = stack._Sstatus
	_rid = []
	for key in global_settings.rasps:
		rasp = global_settings.rasps[key]
		if rasp._stack == _id:
			_rid.append(int(global_settings.rasps[key]._id))
	_x = stack._x
	_y = stack._y
	raspObject = json.JSONEncoder().encode({
                "id": _id,
                "rid":_rid,  
                "power": _power,
                "Sstatus":_Sstatus,
                "x":_x,
                "y":_y
                })
	return raspObject

def get_stacks():
	try:
		stacks = [obj_to_json(global_settings.stacks[key]) for key in global_settings.stacks]
	except:
		stacks = []
	return stacks

def get_stack_by_id(ssid):
        sid = str(ssid)
        stack = global_settings.stacks[sid]
        return obj_to_json(stack)

def ping_rasps_in_stack(nstack):
        print('------------------------------------')
        print("---- Ping command in process... ----")
        print('------------------------------------')
        tmp = 0
        for key in global_settings.rasps:
                if global_settings.rasps[key]._stack == nstack:
                        ip = global_settings.rasps[key]._ip
                        id = global_settings.rasps[key]._id
                        print("ip, id rasp:", ip, id)
                        try:
                                #bash ping command from master to pis
                                sh.ping(ip, "-c 2",_out="/dev/null")
                                global_settings.rasps[id]._Rstatus = "okStatus"
                                print(ip, " is up")
                                date = datetime.datetime.now()
                                date = date.strftime('%d/%m/%Y')
                                rasps_handler.update_rasp_by_id(id,"ping",date,200)
                                tmp = tmp + 1
                        except sh.ErrorReturnCode_1:
                                print("no response from", ip)
                                global_settings.rasps[id]._Rstatus = "koStatus"
        if tmp == 0:
                global_settings.stacks[nstack]._Sstatus = "koStatus"
        else:
                if tmp< int(configRack['rack']['pi_stack']):
                        print("Warning")
                        global_settings.stacks[nstack]._Sstatus = "warningStatus"
                else:
                        global_settings.stacks[nstack]._Sstatus = "okStatus"
        return

