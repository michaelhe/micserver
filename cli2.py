#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import threading
import logging

from micprotcol import SsmMsgHeader

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)


class HeartBeatThd(threading.Thread):

    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sock = sock

    def run(self):
        logging.info('start hb thread')
        try:
            while True:
                logging.info('send ping...')
                send_msg = b'PING'
                send_cmd = 2000
                send_header = SsmMsgHeader.pack_head(send_msg, send_cmd)
                self.sock.sendall(send_header+send_msg)
                time.sleep(15)
        except Exception,e:
            logging.info('HB thread found exception : %s' % e)
            self.sock.close()
            logging.info('%s thread is dead' % self.name)


class Client(object):

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self._head_size = SsmMsgHeader.get_head_size()
        self._data_buffer = bytes()


    def doConnect(self):
        logging.debug('Connect to %s:%s...' % (self.host, self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.connect((self.host, self.port))
        logging.debug('Connected , sock is %s ' % self.sock )

    def doPing(self):
        logging.info('start to ping thread...')
        
        #self.pingthd = HeartBeatThd(self.sock)
        #self.pingthd.start()

        for i in range(0, 1):
            HeartBeatThd(self.sock).start()

    def waitControl(self):
        logging.info('start to control thread...')  

        while True:
            logging.debug('waiting for control message ...')
            msg = self.sock.recv(1024)
            # logging.debug('receive message : %s' %  msg)

            if not msg:
                self.retry()

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
                    logging.debug('handle_msg : %s ...' % body)
                    self.handle_msg(head_pack, body)

                    self._data_buffer = self._data_buffer[self._head_size + body_size:]

        logging.info( 'main thread is gone')
            

    def handle_msg(self, head_pack, body):
        logging.debug('Get response : %s ...' % body)

    def run(self):
        try:
            self.doConnect()
            self.doPing()
            self.waitControl()           
        except Exception,e:
            logging.info('Main exception : %s' % e)
            self.retry()
        
    def retry(self):
        logging.error('lose connect, wait 5s and retry...') 
        self.delete()
        time.sleep(5)
        self.run()           

    def delete(self):
        logging.debug('delete this client ... ')
        self.sock.close()
        self._data_buffer = bytes()

if __name__=='__main__':
    try:
        client = Client('127.0.0.1',6222)
        client.run()
    except KeyboardInterrupt:
        logging.error('Found KeyboardInterrupt...')
        client.delete()
    except Exception,e:
        logging.info('found exception : %s' % e)
        client.delete()
        

