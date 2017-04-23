#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import threading
import logging
import time
import json

from micprotcol import SsmMsgHeader
from LightMysql import LightMysql

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)

lock = threading.Lock()

class CliLink(threading.Thread):

    def __init__(self, conn, addr, db):
        threading.Thread.__init__(self)
        #self.setName('tcpserver')
        self.setDaemon(True)
        self.addr = addr
        self.conn = conn
        TcpServer.clients_connected[addr] = conn
        self._data_buffer = bytes()
        self._head_size = SsmMsgHeader.get_head_size()
        self.db = db

        #self.conn.settimeout(3)

    def delete(self):
        logging.debug('CliLink(%s) is to be destroy' % self.conn)
        if self.addr in TcpServer.clients_connected.viewkeys():
            if lock.acquire():
                TcpServer.clients_connected.pop(self.addr)
                self.conn.close()
                lock.release()

    def handle_msg(self, head_pack, body):

        if head_pack[2] == 1001:
            logging.debug('get %s from client ...' % body)
            resp_msg = b'PONG'
            resp_cmd = 1002
        elif head_pack[2] == 2000:
            logging.debug('get %s from client ...' % body)
            data = json.loads(body)
            port = data.items()[0][0]
            flow = data.items()[0][1]
            sql = "insert into t_flow_data values(now(), %s, %s)"
            self.db.dml(sql, (port, flow))
            resp_msg = b'success'
            resp_cmd = 3000
        else:
            logging.debug('I can not know this msg: %s' % body)
            resp_msg = b'unavailable'
            resp_cmd = 404

        resp_header = SsmMsgHeader.pack_head(resp_msg, resp_cmd)
        self.conn.sendall(resp_header+resp_msg)

        #elif 

    def run(self):
        while True:
            try:
                logging.debug('waiting for message ...')
                msg = self.conn.recv(2048)
                logging.debug('receive message : %s' %  msg)

                if not msg:
                    self.delete()
                    #time.sleep(0.1)
                    break

                if msg:
                    self._data_buffer += msg
                    while True:
                        logging.debug('data buffer length is %s' % len(self._data_buffer))
                        if len(self._data_buffer) < self._head_size:
                            break

                        head_pack = SsmMsgHeader.unpack_head(
                            self._data_buffer[:self._head_size])
                        #logging.info('head_pack is %s' % head_pack)

                        body_size = head_pack[1]

                        if len(self._data_buffer) < self._head_size + body_size :
                            break
                            
                        body = self._data_buffer[self._head_size:self._head_size + body_size]

                        self.handle_msg(head_pack, body)

                        self._data_buffer = self._data_buffer[self._head_size + body_size:]
            #except TypeError as e:
            #    logging.error('the message is unavailable pack')
            except Exception, e:
                logging.error('CLI link run find exception : %s' %  e)
                self.delete() 
                time.sleep(5)               
                break

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
            logging.debug('clients are : %s' % TcpServer.clients_connected.viewkeys())
            time.sleep(5)

class TcpServer(object):

    clients_connected = {}
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

        dbconfig = {
            'host':'127.0.0.1',
            'port': 3306,
            'user':'michael',
            'passwd':'michael',
            'db':'db_test',
            'charset':'utf8'}

        self.db = LightMysql(dbconfig)

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
            
            client = CliLink(conn, addr, self.db)
            client.start()


    def close(self):
        if self.socket:
            self.socket.close()

def main():
    host = '0.0.0.0'
    port = 6221

    try:
        tcp_server = TcpServer(host, port)
        tcp_server.run()
    except KeyboardInterrupt:
        print 'Ctrl+C pressed... Shutting Down'
        tcp_server.close()
    except Exception,e:
        logging.error('find error in main function %s' % e)

if __name__=='__main__':
    main()
