#!/usr/bin/env python
#encoding=utf-8
'''db'''
import config
# import tornado.database
import torndb

NewsDatabase = torndb.Connection(
    "127.0.0.1",
    "cippusrightpeter",
    "test",
    "woludie",
)
