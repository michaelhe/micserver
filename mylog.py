#!/usr/bin/python
# -*- coding: UTF-8 -*-


import logging

# setup logger
logger = logging.getLogger()
handler = logging.StreamHandler()
fmt='%(asctime)s | %(levelname)-8s | %(message)s'
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt,datefmt)
        
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')