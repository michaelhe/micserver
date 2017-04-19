#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import logging
import time

logging.basicConfig(
	level = logging.DEBUG,
	format = '%(threadName)s | %(message)s' 
)

def daemon():
	logging.debug('Starting...')
	time.sleep(2)
	logging.debug('Exit!!!')

def non_daemon():
	logging.debug('Starting...')
	time.sleep(1)
	logging.debug('Exit!!!')

d = threading.Thread(name='daemon',target=daemon)
d.setDaemon(True)
t = threading.Thread(name='non-daemon',target=non_daemon)

d.start()
t.start()
d.join()

