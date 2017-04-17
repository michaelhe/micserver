#!/usr/bin/env python
import signal
import socket  
import sys
import logging

# Setup logger
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


# Setup  control+c 
# Register signal handlers
def receive_signal(signum, stack):
    print 'I will exit...'
    sys.exit(0)
signal.signal(signal.SIGINT, receive_signal)


if __name__ == '__main__':

	address = ('127.0.0.1', 30000)  
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	s.bind(address)  
	logger.info('start udp server...')

	try:
		while True:  
		    data, addr = s.recvfrom(2048)
		    logger.info("received:", data, "from", addr[0])
	except Exception,e:
	    print e
	  
	s.close()  
