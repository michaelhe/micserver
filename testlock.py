#!/usr/bin/env python
#-*- coding:utf-8 -*-


import threading
import time
import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)

lock = threading.Lock()

class A(object):
    
    num = 0

class Add(threading.Thread):

    def __init__(self, i):
        threading.Thread.__init__(self)
        self.setName('add-thread-%s' % i)

    def run(self):
        if lock.acquire():
            time.sleep(0.1)
            A.num += 1 
            logging.info('A.num is %s' % A.num)
            lock.release()

class Del(threading.Thread):

    def __init__(self, i):
        threading.Thread.__init__(self)
        self.setName('del-thread-%s' % i)

    def run(self):
        if lock.acquire():
            time.sleep(0.1)
            A.num -= 1
            logging.info('A.num is %s' % A.num)
            lock.release()

if __name__=='__main__':

    for i in range(0,5):
        Add(i).start()

    for i in range(0,5):
        Del(i).start()


