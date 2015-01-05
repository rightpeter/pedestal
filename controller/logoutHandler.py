#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import re
import time
import json
import tornado.web
import tornado.ioloop
import tornado.httpclient
# tornado 3.x nolonger have this. use torndb
#import tornado.database
import torndb
import math
import httplib
import json
import pickle
import datetime
import threading
from config import *
from model import *
import util.myTools as myTools

class LogoutHandler(myTools.BaseHandler):
    def get(self):
        url = self.get_cookie('url')
        self.clear_cookie('name')
        self.clear_cookie('guest')
        self.clear_cookie('login')
        self.redirect(url)

