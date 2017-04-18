#!/usr/bin/env python
import signal
import socket  
import sys
import logging
import getopt
import string

# Setup logger
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def usage():
    print """
    -h --help             print the help
    -l --list             Maximum number of connections
    -p --port             To monitor the port number  
    """

# Setup  control+c 
# Register signal handlers
def receive_signal(signum, stack):
    print 'I will exit...'
    sys.exit(0)


def main(port):
	address = ('127.0.0.1', port)  
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	s.bind(address)
	try:
		while True:  
		    data, addr = s.recvfrom(2048)
		    logger.info("received: %s , from %s " % (data, addr[0]))
	except Exception,e:
	    print e
	s.close()  


if __name__ == '__main__':
	# Setup opts & args
	list=50
	port=30000
	opts, args = getopt.getopt(sys.argv[1:], "hp:l:",["help","port=","list="])
	for op, value in opts:
	    if op in ("-l","--list"):
	        list = string.atol(value)
	    elif op in ("-p","--port"):
	        port = string.atol(value)
	    elif op in ("-h"):
	        usage()
	        sys.exit()

	logger.info('start udp server...')
	# Setup signal
	signal.signal(signal.SIGINT, receive_signal)

	main(port)


