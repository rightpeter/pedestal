#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import re
import time
import tornado
import torndb
import math
import httplib
import pickle
import datetime
from config import *
from model import *
import util.myTools as myTools

BaseHandler = myTools.BaseHandler

class IndoorHandler(myTools.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = myTools.get_current_user(self)
        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('indoor/WorldMap.html', user=user, url=url, login_state=login_state)

class IndoorMapHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        try:
            bid = int(self.get_argument('bid'))
            level = int(self.get_argument('level'))
            indoor_map_file = open('/home/rightpeter/github/Geography_Cloud/static/buildings/%s/%s.svg' % (bid, level))
        except Exception, e:
            indoor_map_file = open('/home/rightpeter/github/Geography_Cloud/static/buildings/1/1.svg')
            print e

        indoor_map = indoor_map_file.read()
        elements=[{'href': '/app/indoor/map?bid=1&level=1',
                    'content': '一楼'},
                  {'href': '/app/indoor/map?bid=1&level=2',
                    'content': '二楼'},
                  {'href': '/app/indoor/map?bid=1&level=3',
                    'content': '三楼'},
                  {'href': '/app/indoor/map?bid=1&level=4',
                    'content': '四楼'},
                  {'href': '/app/indoor/map?bid=1&level=5',
                    'content': '五楼'}]
        lid='indoor_map'
        lclass='indoor_list'
        
        user = myTools.get_current_user(self)
        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('indoor/mapdemo.html', user=user, url=url,
                login_state=login_state, lid=lid, lclass=lclass,
                elements=elements, indoor_map=indoor_map)
        
