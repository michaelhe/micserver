#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket
import time
import threading
import logging


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
                self.sock.sendall(b'ping')
                time.sleep(5)
        except Exception,e:
            logging.info('HB thread found exception : %s' % e)
            self.sock.close()


class Client(object):

    def __init__(self, host, port):

        self.host = host
        self.port = port


    def doConnect(self):
        logging.debug('Connect to %s:%s...' % (self.host, self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect((self.host,self.port))

    def doPing(self):
        logging.info('start to ping thread...')
        self.pingthd = HeartBeatThd(self.sock)
        self.pingthd.start()

    def waitControl(self):
        logging.info('start to control thread...')  
        while True:
            control_msg=self.sock.recv(1024)
            logging.info('control_msg msg is %s' % control_msg)
            if not control_msg:
                logging.info('control_msg msg is null')
                self.delete()

    def run(self):
        try:
            self.doConnect()
            self.doPing()
            self.waitControl()
        except socket.error:
            logging.error('Socket error, wait 5s and retry...')
            self.delete()
            time.sleep(5)
            self.run()          
        except Exception,e:
            logging.info('waitControl found exception : %s' % e)
            self.delete()
            time.sleep(5)
            self.run()

    def delete(self):
        self.sock.close()


if __name__=='__main__':
    try:
        client = Client('linode.ylkb.net',6221)
        client.run()
    except KeyboardInterrupt:
        logging.error('Found KeyboardInterrupt...')
        client.delete()
    except Exception,e:
        logging.info('found exception : %s' % e)
        client.delete()
        

