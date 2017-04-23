#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import struct
import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s | %(threadName)s | %(message)s' 
)

'''
定义包的结构，使用struct来打包
[version, body_len, cmd]
version : 版本号
body_len : 为后面的文本的长度
cmd : 为指令ID
cmd-1001 : 为PING报文
cmd-1002 : 为PONG报文
cmd-2000 : 为client->server上报的数据报文
cmd-3000 : 为server->client下发的控制报文
'''

class SsmMsgHeader(object):

    version = 1
    header_fmt = '!3I'

    @classmethod
    def get_head_size(cls):
        return struct.calcsize(cls.header_fmt)

    @classmethod
    def pack_head(cls, data, cmd):
        body_len = str(data).__len__()
        header = [cls.version, body_len, cmd]
        return struct.pack(cls.header_fmt, *header)

    @classmethod
    def unpack_head(cls, data):
        return struct.unpack(cls.header_fmt, data)


if __name__=='__main__':
    logging.info(SsmMsgHeader.get_header_len())
    hp = SsmMsgHeader.pack_header('hello world', 2000)
    logging.info(hp)
    logging.info(SsmMsgHeader.unpack_header(hp))





