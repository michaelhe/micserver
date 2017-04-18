#!/usr/bin/env python

import socket  
  
address = ('127.0.0.1', 30000)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

s.sendto(b'aaa', address) 
s.close() 
