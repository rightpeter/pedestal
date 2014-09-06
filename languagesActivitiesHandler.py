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

class LanguagesActivitiesHandler(BaseHandler):
    def get(self):
        user = myTools.get_current_user(self)
        self.set_cookie("url", self.request.uri)
        url = self.request.uri

        login_state = self.get_cookie('login')
        
        self.render('languages_activities.html', user=user, url=url,
                login_state=login_state)


