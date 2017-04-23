#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import threading
import logging
import time

from micprotcol import SsmMsgHeader

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)

lock = threading.Lock()

class CliLink(threading.Thread):

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        #self.setName('tcpserver')
        self.setDaemon(True)
        self.addr = addr
        self.conn = conn
        TcpServer.clients_connected[(addr)] = conn
        self._data_buffer = bytes()
        self._head_size = SsmMsgHeader.get_head_size()

        #self.conn.settimeout(3)

    def delete(self):
        #logging.debug('CliLink(%s) is to be destroy' % self.conn)
        if self.addr in TcpServer.clients_connected.viewkeys():
            if lock.acquire():
                TcpServer.clients_connected.pop(self.addr)
                self.conn.close()
                lock.release()

    def handle_msg(self, head_pack, body):

        if body == 'PING':
            logging.debug('get PING from client ...')
            resp_msg = b'PONG'
            resp_cmd = 1002
            resp_header = SsmMsgHeader.pack_head(resp_msg, resp_cmd)
            self.conn.sendall(resp_header+resp_msg)
        #elif 

    def run(self):
        while True:
            try:
                logging.debug('waiting for message ...')
                msg = self.conn.recv(2048)
                logging.debug('receive message : %s' %  msg)
            except Exception,e:
                logging.debug('CLI link run find exception : %s' %  e)
                time.sleep(5)
                self.delete()
                break

            if not msg:
                self.delete()
                break

            if msg:
                self._data_buffer += msg
                while True:
                    if len(self._data_buffer) < self._head_size:
                        break
                    head_pack = SsmMsgHeader.unpack_head(
                        self._data_buffer[:self._head_size])

                    body_size = head_pack[1]

                    if len(self._data_buffer) < self._head_size + body_size :
                        break
                        
                    body = self._data_buffer[self._head_size:self._head_size + body_size]

                    self.handle_msg(head_pack, body)

                    self._data_buffer = self._data_buffer[self._head_size + body_size:]

        logging.info( '%s is gone' % self.name)
        


class CountLink(threading.Thread):

    def __init__(self):
        logging.info('starting counting link thread ...')
        threading.Thread.__init__(self)
        self.setName('Thread-CountLink')
        self.setDaemon(True)

    def run(self):
        while True:
            logging.info('clients: %s' % len(TcpServer.clients_connected))
            logging.info('clients are : %s' % TcpServer.clients_connected.viewkeys())
            time.sleep(5)

class TcpServer(object):

    clients_connected = {}
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        logging.debug('server(%s:%s) initial completed!' %  
                      (self.host, self.port))

    def run(self):

        # 启动统计线程，统计当前连接数
        count_link = CountLink()
        count_link.start()

        while True:
            logging.debug('waiting for linking from client ...')
            conn, addr = self.socket.accept()
            logging.debug('connected by: %s:%s'  % (addr[0], addr[1]))
            
            client = CliLink(conn, addr)
            client.start()


    def close(self):
        if self.socket:
            self.socket.close()

def main():
    host = '127.0.0.1'
    port = 6221

    try:
        tcp_server = TcpServer(host, port)
        tcp_server.run()
    except KeyboardInterrupt:
        print 'Ctrl+C pressed... Shutting Down'
        tcp_server.close()

if __name__=='__main__':
    main()
