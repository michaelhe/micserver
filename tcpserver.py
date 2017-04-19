#!/usr/bin/env python
import socket
import threading
import logging
import time

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)

class TcpLink(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self);
        #self.setName('tcpserver')
        self.setDaemon(True)
        self.conn = conn
        self.conn.settimeout(3)

    def run(self):
        
        while True:
            try:
                msg = self.conn.recv(2048)
                logging.debug('receive message : %s' %  msg)
            except Exception,e:
                logging.debug('find exception : %s' %  e)
                time.sleep(5)
                self.conn.close()
                break

            if not msg:
                logging.debug( '%s is over' % self.name)
                self.conn.close()
                break

            self.conn.sendall(msg)
            if msg == 'byebye':
                logging.debug( '%s is over' % self.name)
                self.conn.close()
                break

        logging.debug( '%s is gone' % self.name)

def main():
    HOST = 'localhost'
    PORT = 6221
    ADDRESS = (HOST, PORT)

    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    S.bind(ADDRESS)
    S.listen(5)

    logging.debug('server started, listen on %s:%s ' %  (HOST,PORT))

    try:
        while True:
            conn, addr = S.accept()
            logging.debug('connected by: %s:%s'  % (addr[0],addr[1]))
            client = TcpLink(conn)
            client.start()

    except KeyboardInterrupt:
        print 'Ctrl+C pressed... Shutting Down'
        S.close()

if __name__=='__main__':
    main()
