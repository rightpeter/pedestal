#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import re
import time
import tornado.web
import tornado.ioloop
import tornado.httpclient
# tornado 3.x nolonger have this. use torndb
#import tornado.database
import torndb
import math
import httplib
import pickle
import datetime
import threading
from config import *
from model import *
import  util.myTools as myTools

class HomeHandler(myTools.BaseHandler):
    @tornado.web.authenticated
    def get(self, home_id):
        home_name = myTools.get_name_by_id(home_id)
        user = myTools.get_current_user(self)
        avatar_ext = myTools.get_avatar_ext_by_id(home_id)
        if avatar_ext:
            avatar_file = '%s%s' % (home_id, avatar_ext)
            # print 'avatar_file: ', avatar_file 
            if not os.path.exists(avatar_path + avatar_file):
                avatar_file = 'default.jpg'
        else:
            avatar_file = 'default.jpg'

        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('home.html', home_name=home_name, user=user,
                avatar_file=avatar_file, url=url,
                login_state=login_state)


