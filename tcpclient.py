#!/usr/bin/env python
import socket

HOST = 'localhost'
PORT = 6221
ADDRESS = (HOST, PORT)

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect(ADDRESS)

while 1:
    reply = raw_input('input:')
    if reply == 'bye':
        break
    S.sendall(reply)
    msg = S.recv(2048)
    print '%s says: %s' % (HOST, msg)
    if msg == 'bye':
        break

S.close()
