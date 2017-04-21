#!/usr/bin/env python
import socket
import time
import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)

HOST = 'localhost'
PORT = 6221
ADDRESS = (HOST, PORT)

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#S.settimeout(5)
logging.info('connect to server...')
S.connect(ADDRESS)
S.settimeout(3)

#try:
#	S.recv(1024)
#except Exception,e:
#    S.close()

while True:
    reply = raw_input('input:')
    if reply == 'bye':
        break
    S.sendall(reply)
    msg = S.recv(2048)
    logging.info('%s says: %s' % (HOST, msg))
    if msg == 'bye':
        break

#logging.info('start to sleep...')
#time.sleep(10)

logging.info('end...')
S.close()




