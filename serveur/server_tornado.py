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
from configparser import ConfigParser

rasps = [
    {
        'id': 1,
        'ip': '172.0.0.1',
        'mac': '00:EF:4G:00:45:OP',
        'power': 'On',
        'cpu': '22',
        'Lping': '25/20/1992',
        'stack': '1',
        'Rstatus': 'okStatus',
        'level': '4'
    },
    {
        'id': 2,
        'ip': '172.0.0.2',
        'mac': '00:EF:4B:00:43:OP',
        'power': 'Off',
        'cpu': '46',
        'Lping': '25/20/1992',
        'stack': '2',
        'Rstatus': 'okStatus',        
        'level': '5'
    },
    {
        'id': 3,
        'ip': '172.0.0.3',
        'mac': '00:43:4G:00:45:OP',
        'power': 'On',
        'cpu': '99',
        'Lping': '25/20/1992',
        'stack': '1',
        'Rstatus': 'koStatus', 
        'level': '6'
    },
    {
        'id': 4,
        'ip': '172.0.0.4',
        'mac': '00:43:4G:00:45:OP',
        'power': 'On',
        'cpu': '97',
        'Lping': '25/20/1992',
        'stack': '3',
        'Rstatus': 'koStatus', 
        'level': '6'
    },
    {
        'id': 5,
        'ip': '172.0.0.5',
        'mac': '00:43:4G:00:45:OQ',
        'power': 'Off',
        'cpu': '92',
        'Lping': '25/20/1992',
        'stack': '3',
        'Rstatus': 'warningStatus', 
        'level': '4'
    },
    {
        'id': 6,
        'ip': '172.0.0.6',
        'mac': '00:43:4G:00:45:OQ',
        'power': 'Off',
        'cpu': '92',
        'Lping': '25/20/1992',
        'stack': '2',
        'Rstatus': 'okStatus', 
        'level': '4'
    },
    {
        'id': 7,
        'ip': '172.0.0.7',
        'mac': '00:EF:4G:00:45:OP',
        'power': 'On',
        'cpu': '22',
        'Lping': '25/20/1992',
        'stack': '1',
        'Rstatus': 'okStatus', 
        'level': '4'
    },
    {
        'id': 8,
        'ip': '172.0.0.2',
        'mac': '00:EF:4B:00:43:OP',
        'power': 'Off',
        'cpu': '46',
        'Lping': '25/20/1992',
        'stack': '3',
        'Rstatus': 'koStatus', 
        'level': '5'
    },
    {
        'id': 9,
        'ip': '172.0.0.3',
        'mac': '00:43:4G:00:45:OP',
        'power': 'On',
        'cpu': '99',
        'Lping': '25/20/1992',
        'stack': '1',
        'Rstatus': 'okStatus', 
        'level': '6'
    },
    {
        'id': 10,
        'ip': '172.0.0.4',
        'mac': '00:43:4G:00:45:OP',
        'power': 'On',
        'cpu': '97',
        'Lping': '25/20/1992',
        'stack': '2',
        'Rstatus': 'okStatus', 
        'level': '6'
    },
    {
        'id': 11,
        'ip': '172.0.0.5',
        'mac': '00:43:4G:00:45:OQ',
        'power': 'Off',
        'cpu': '92',
        'Lping': '25/20/1992',
        'stack': '3',
        'Rstatus': 'okStatus', 
        'level': '4'
    },
    {
        'id': 12,
        'ip': '172.0.0.6',
        'mac': '00:43:4G:00:45:OQ',
        'power': 'Off',
        'cpu': '92',
        'Lping': '25/20/1992',
        'stack': '2',
        'Rstatus': 'okStatus', 
        'level': '4'
    },
    {
        'id': 13,
        'ip': '172.0.0.7',
        'mac': '00:EF:4G:00:45:OP',
        'power': 'On',
        'cpu': '22',
        'Lping': '25/20/1992',
        'stack': '4',
        'Rstatus': 'koStatus', 
        'level': '4'
    },
    {
        'id': 14,
        'ip': '172.0.0.2',
        'mac': '00:EF:4B:00:43:OP',
        'power': 'Off',
        'cpu': '46',
        'Lping': '25/20/1992',
        'stack': '4',
        'Rstatus': 'okStatus', 
        'level': '5'
    },
    {
        'id': 15,
        'ip': '172.0.0.3',
        'mac': '00:43:4G:00:45:OP',
        'power': 'On',
        'cpu': '99',
        'Lping': '25/20/1992',
        'stack': '4',
        'Rstatus': 'okStatus', 
        'level': '6'
    },
    {
        'id': 16,
        'ip': '172.0.0.4',
        'mac': '00:43:4G:00:45:OP',
        'power': 'On',
        'cpu': '97',
        'Lping': '25/20/1992',
        'stack': '4',
        'Rstatus': 'okStatus', 
        'level': '6'
    },
    {
        'id': 17,
        'ip': '172.0.0.5',
        'mac': '00:43:4G:00:45:OQ',
        'power': 'Off',
        'cpu': '92',
        'Lping': '25/20/1992',
        'stack': '5',
        'Rstatus': 'koStatus', 
        'level': '4'
    },
    {
        'id': 18,
        'ip': '172.0.0.6',
        'mac': '00:43:4G:00:45:OQ',
        'power': 'Off',
        'cpu': '92',
        'Lping': '25/20/1992',
        'stack': '5',
        'Rstatus': 'okStatus', 
        'level': '4'
    }                                   
]

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
            self._state = tornado.ioloop.IOLoop.ERROR | state
            self.ioloop.add_handler(
                self.socket.fileno(), self._handle_events, self._state)
        elif not self._state & state:
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
        self._read_timeout = self.ioloop.add_timeout( time.time() + timeout,
            self.check_read_callback )
        self._add_io_state(self.ioloop.READ)

    def check_read_callback(self):
        if self._read_callback:
            # XXX close socket?
            self._read_callback(data = 'timeout, no response', ip = None, code = 404);

    def _handle_read(self):
        if self._read_timeout:
            self.ioloop.remove_timeout(self._read_timeout)
        if self._read_callback:
            try:
                datatmp, addr = self.socket.recvfrom(1024)
                data = datatmp.decode("utf-8")
                code_status = 200
                ip = addr[0]
            except:
                # conn refused??
                data = None
                ip = None
                code_status = 404
            self._read_callback(data= data,ip = ip, code = code_status);
            self._read_callback = None

    def _handle_events(self, fd, events):
        if events & self.ioloop.READ:
            self._handle_read()
        if events & self.ioloop.ERROR:
            logging.error('%s event error' % self)

class RaspGetHandler(tornado.web.RequestHandler):
    def get(self, rasp_id):
        self._status = 200
        rasp = [rasp for rasp in rasps if rasp['id'] == rasp_id]
        if len(rasp) == 0:
            self._status = 404
        response = {'rasp': rasp[0]}
        self.set_status(self._status)
        self.write(json_encode(response))

class RaspsOptionsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
    def get(self):
        # read values from a section
        actions = [key for key in config['rasps']]
        response = {'actions': actions}
        self.write(json_encode(response))

class RaspsGetHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        self.add_header('Access-Control-Allow-Headers', 'X-Requested-With')
    def get(self):
        response = {'rasps': [rasp for rasp in rasps]}
        self.write(json_encode(response))

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
        if jsonRequestAction["action"] == "ping":
            print(config['rasps']['Ping'])
            #Variable provisoire en attendant le mapping
            hostname = "127.0.0.1"
            response = os.system( config['rasps']['Ping'] +' '+ hostname + "> /dev/null 2>&1")
            if response == 0:
                date = datetime.datetime.now()
                date = date.strftime('%d/%m/%Y')
                self.respond(date , 200)
            else:
                self.respond( hostname + "is down", 404)
        else:
            tmp = "rasps:"+jsonRequestAction["action"]
            MESSAGE = bytes(tmp,'utf-8')
            UDP_IP = jsonRequestAction["ip"]
            UDP_PORT = jsonRequestAction["Port"]
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.setblocking(False)
            s = UDPStream(udpsock)
            udpsock.sendto(MESSAGE,(UDP_IP, UDP_PORT))
            dataObject = yield tornado.gen.Task( s.read_chunk )
            code_status = dataObject[1]["code"]
            data = dataObject[1]["data"]
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

application = tornado.web.Application([
    (r"/api/v1.0/rasps", RaspsGetHandler),
    (r"/api/v1.0/rasps/execute", RaspsActionsHandler),
    (r"/api/v1.0/rasps/options", RaspsOptionsHandler),
    (r"/api/v1.0/rasps/([0-9]+)", RaspGetHandler)
])

if __name__ == "__main__":
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
