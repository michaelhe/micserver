#!/usr/bin/env python
import socket
import threading

HOST = 'localhost'
PORT = 6221
ADDRESS = (HOST, PORT)

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.bind(ADDRESS)
S.listen(5)

while 1:
    conn, addr = S.accept()
    print 'connected by:', addr[0]
    def job(conn):
        while 1:
            msg = conn.recv(2048)
            print '%s says: %s' % (addr[0], msg)
            reply = raw_input('input:')
            conn.sendall(reply)
    t = threading.Thread(target=job, args=[conn])
    t.daemon = True
    t.start()

S.close()
