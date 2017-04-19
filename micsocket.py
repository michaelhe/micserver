#!/usr/bin/python
# -*- coding: UTF-8 -*-

import SocketServer
import logging
import time

logging.basicConfig(
	level = logging.DEBUG,
	format = '%(threadName)s | %(message)s' 
)

class MicSocket(SocketServer.BaseRequestHandler):

	def handle(self):
		data = self.request[0].strip()
		addr = self.request[1]
		logging.debug('receive data %s from %s' % (data,self.client_address[0]))

if __name__=='__main__':

	address = ('127.0.0.1',30000)
	server = SocketServer.UDPServer(address, MicSocket)
	server.serve_forever()