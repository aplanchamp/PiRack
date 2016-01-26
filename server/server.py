import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen
import time
import json
import logging
import struct
from tornado.escape import json_encode
import sys
import socket
import os
import datetime
from newInstall import log_monitor
from newInstall import global_settings
from configparser import ConfigParser
from handlers import rasps_handler
from handlers import stacks_handler
from newInstall import stack_power

global_settings.init()
log_monitor.get_rasps_from_csv()
log_monitor.get_stacks_from_csv()

PORT = 1026

# instantiate
config = ConfigParser()

# parse existing file
config.read('configuration.ini')

class UDPStream(object):
	def __init__(self, socket, in_ioloop=None):
		self.socket = socket
		self._state = None
		self._read_callback = None
		self.ioloop = in_ioloop or tornado.ioloop.IOLoop.instance()

	def _add_io_state(self, state):
		if self._state is None:
			print("None")
			self._state = tornado.ioloop.IOLoop.ERROR | state
			self.ioloop.add_handler(self.socket.fileno(), self._handle_events, self._state)
		elif not self._state & state:
			print("Ok")
			self._state = self._state | state
			self.ioloop.update_handler(self.socket.fileno(), self._state)

	def send(self,msg):
		return self.socket.send(msg)

	def recv(self,sz):
		return self.socket.recv(sz)

	def close(self):
		self.ioloop.remove_handler(self.socket.fileno())
		self.socket.close()
		self.socket = None

	def read_chunk(self, callback=None, timeout=10):
		self._read_callback = callback
		print("addtime")
		self._read_timeout = self.ioloop.add_timeout( time.time() + timeout,self.check_read_callback )
		self._add_io_state(self.ioloop.READ)

	def check_read_callback(self):
		if self._read_callback:
			# XXX close socket?
			print("timecall")
			self._read_callback(data = 'timeout, no response', ip = None, code = 404);

	def _handle_read(self):
		if self._read_timeout:
			print("handler1")
			self.ioloop.remove_timeout(self._read_timeout)
		if self._read_callback:
			print("handler2")
			try:
				print("handler3")
				datatmp, addr = self.socket.recvfrom(1024)
				print(datatmp, addr)
				data = datatmp.decode("utf-8")
				print("DAta", data)
				code_status = 200
				ip = addr[0]
			except:
				print("handler4")
				# conn refused??
				data = None
				ip = None
				code_status = 404
			self._read_callback(data= data,ip = ip, code = code_status);
			self._read_callback = None

	def _handle_events(self, fd, events):
		if events & self.ioloop.READ:
			print("Read")
			self._handle_read()
		if events & self.ioloop.ERROR:
			print("Error")
			logging.error('%s event error' % self)

def respond(self, data, code=200):
	self.set_status(code)
	self.write(data)
	self.finish()

class RaspGetHandler(tornado.web.RequestHandler):
	def get(self, id):
		status = 200
		rasp = rasps_handler.get_rasp_by_id(id)
		if len(rasp) == 0:
			status = 404
		respond(self,json.loads(rasp), status)

class InstallationHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
                self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
                self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
                self.add_header('Access-Control-Allow-Headers', 'Content-Type')

        def get(self):
                status = 200
                log_monitor.install()
                log_monitor.get_rasps_from_csv()
                log_monitor.get_stacks_from_csv()
                stacks = stacks_handler.get_stacks()
                if len(stacks) == 0:
                       status = 404
                response = {'stacks': [json.loads(stack) for stack in stacks]}
                print(response)
                respond(self, response, status)

class RaspsOptionsHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
		self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
	def get(self):
		# read values from a section
		status = 200
		actions = [key for key in config['rasps']]
		if len(actions) == 0:
			status = 404
		response = {'actions': actions}
		respond(self,json_encode(response),status)

class RaspsGetHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
		self.add_header('Access-Control-Request-Method', 'POST')
		self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
	def get(self):
		status = 200
		rasps = rasps_handler.get_rasps()
		if len(rasps) == 0:
			status = 404
		response = {'rasps': [json.loads(rasp) for rasp in rasps]}
		respond(self,response,status)

class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)

class RaspsActionsHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
		self.add_header('Access-Control-Request-Method', 'POST')
		self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
		self.add_header('Access-Control-Allow-Headers', 'Content-Type')
	@tornado.gen.coroutine
	def post(self):
		requestAction = self.request.body
		strRequestAction = requestAction.decode("utf-8")
		jsonRequestAction = json.loads(strRequestAction)
		slave_id = str(jsonRequestAction["id"])
		print(global_settings.rasps)
		rasp = global_settings.rasps[slave_id]
		IP = rasp._ip
		if jsonRequestAction["action"] == "ping":
			#Variable provisoire en attendant le mapping
			response = os.system( config['rasps']['Ping'] +' '+ IP + "> /dev/null 2>&1")
			if response == 0:
				date = datetime.datetime.now()
				date = date.strftime('%d/%m/%Y')
				print(rasp._id)
				rasps_handler.update_rasp_by_id(slave_id,"ping",date,200)
				self.respond(date , 200)
			else:
				self.respond(IP + " is down", 404)
		else:
			MESSAGE = " "
			tmp = "rasps:"+jsonRequestAction["action"]
			MESSAGE = bytes(tmp,'utf-8')
			udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			udpsock.setblocking(False)
			s = UDPStream(udpsock)
			udpsock.sendto(MESSAGE,(IP, PORT))
			dataObject = yield tornado.gen.Task( s.read_chunk )
			code_status = dataObject[1]["code"]
			data = dataObject[1]["data"]
			rasps_handler.update_rasp_by_id(slave_id,jsonRequestAction["action"],data,code_status)
			ip = dataObject[1]["ip"]
			print("DATA:", data)
			print("CODE:", code_status)
			print("IP:", ip)
			self.respond(data, code_status)
	def options(self):
		self.write("")

	def respond(self, data, code=200):
                self.set_status(code)
                self.write(JSONEncoder().encode({
                        "status": code,
                        "data": data
                }))
                self.finish()

class StacksGetHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
                self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
                self.add_header('Access-Control-Request-Method', 'POST')
                self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
        def get(self):
                status = 200
                stacks = stacks_handler.get_stacks()
                if len(stacks) == 0:
                        status = 404
                response = {'stacks': [json.loads(stack) for stack in stacks]}
                respond(self,response,status)

class StacksOptionsHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
                self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
                self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
        def get(self):
                # read values from a section
                status = 200
                actions = [key for key in config['stacks']]
                if len(actions) == 0:
                        status = 404
                response = {'actions': actions}
                respond(self,json_encode(response),status)

class StackGetHandler(tornado.web.RequestHandler):
        def get(self, id):
                status = 200
                stack = stacks_handler.get_stack_by_id(id)
                if len(stack) == 0:
                        status = 404
                respond(self,json.loads(stack), status)

class StacksActionsHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
                self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
                self.add_header('Access-Control-Request-Method', 'POST')
                self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
                self.add_header('Access-Control-Allow-Headers', 'Content-Type')
        @tornado.gen.coroutine
        def post(self):
                requestAction = self.request.body
                strRequestAction = requestAction.decode("utf-8")
                jsonRequestAction = json.loads(strRequestAction)
                stack_id = int(jsonRequestAction["id"])
                if jsonRequestAction["action"] == "ping":
                        print("-----------Pinging stack-----------")
                        id_str = jsonRequestAction["id"]
                        stacks_handler.ping_rasps_in_stack(id_str)
                elif jsonRequestAction["action"] == "shutdown":
                        stack_power.powerup_stack(stack_id)
                elif jsonRequestAction["action"] == "reboot":
                        stack_power.powerdown_stack(stack_id)
                        time.sleep(1)
                        stack_power.powerup_stack(stack_id)       
                else:
                        tmp = "rasps:"+jsonRequestAction["action"]
                        MESSAGE = bytes(tmp,'utf-8')
                        print(stacks_handler.get_rasps_from_stack(stack_id))
                        rid = stacks_handler.get_rasps_from_stack(stack_id)
                        for id in rid:
                               str_id = str(id)
                               rasp = global_settings.rasps[str_id]
                               IP = rasp._ip
                               print("ip", IP)
                               udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                               udpsock.setblocking(False)
                               s = UDPStream(udpsock)
                               udpsock.sendto(MESSAGE,(IP, PORT))
                               dataObject = yield tornado.gen.Task( s.read_chunk )
                               code_status = dataObject[1]["code"]
                               data = dataObject[1]["data"]
                               rasps_handler.update_rasp_by_id(str_id,jsonRequestAction["action"],data,code_status)
                               ip = dataObject[1]["ip"]
                               print("DATA:", data)
                               print("CODE:", code_status)
                               print("IP:", ip) 

 
        def options(self):
                self.write("")                  

application = tornado.web.Application([
    	(r"/api/v1.0/rasps", RaspsGetHandler),
    	(r"/api/v1.0/rasps/execute", RaspsActionsHandler),
    	(r"/api/v1.0/rasps/options", RaspsOptionsHandler),
    	(r"/api/v1.0/rasps/([0-9]+)", RaspGetHandler),
        (r"/api/v1.0/stacks", StacksGetHandler),
        (r"/api/v1.0/stacks/execute", StacksActionsHandler),
        (r"/api/v1.0/stacks/options", StacksOptionsHandler),
        (r"/api/v1.0/stacks/([0-9]+)", StackGetHandler),
	(r"/api/v1.0/installation", InstallationHandler)
])

if __name__ == "__main__":
	application.listen(5000)
	tornado.ioloop.IOLoop.instance().start()
