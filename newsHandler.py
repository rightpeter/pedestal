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
from db import *
from myTools import *
import uimodules

class NewsHandler(BaseHandler):
    def get(self, nnid):
        nid = int(nnid)
        news = myTools.get_a_news(nid)
        news['id'] = news['nid']
        news.pop('nid')
        news_json = json.dumps(news)
        self.write(news_json)

