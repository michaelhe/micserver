#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import threadpool
import time
import logging

# Setup logger
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def now_time2(n):
  logger.info('Starting at %s' % time.ctime())
  time.sleep(n)
  logger.info('Ending at %s' % time.ctime())

def now_time(n):
  logger.info('Starting at %s' % time.ctime())
  time.sleep(n)
  return '%s - Ending at %s' % (n, time.ctime())


def print_now(request, result):
  logger.info('%s - %s' % (request.requestID, result) ) #这里的requestID只是显示下，没实际意义

pool = threadpool.ThreadPool(1)
reqs = threadpool.makeRequests(now_time, range(1, 11), print_now)
[pool.putRequest(req) for req in reqs]
pool.wait()