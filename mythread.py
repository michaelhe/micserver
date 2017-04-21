#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import logging
import time
import LightMysql

# Setup logger
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class DbQurey(threading.Thread):

    def __init__(self,event):
        threading.Thread.__init__(self)
        self.setName('db_query')
        self.event = event
        dbconfig = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'test',
            'passwd': 'test',
            'db': 'db_test',
            'charset':'utf8'}

        self._db = LightMysql.LightMysql(dbconfig)

    def run(self):
        logger.info('thread(%s) is start' % self.name)
        while True:
            if self.event.is_set():
                break
            result = self._db.select('select * from t_test')
            logger.info('db result is %s' % result)
            time.sleep(2)
        logger.info('thread(%s) is exit' % self.name)

if __name__=='__main__':

    event = threading.Event()
    
    db = DbQurey(event)
    db.start()

    logger.info('main thread is over')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info('send exit info to children thread, wait for 2 second...' )
        event.set()
    except Exception, err:
        print 'Exception caught: %s\nClosing...' % err
