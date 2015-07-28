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
import util. myTools as myTools


class LoginHandler(myTools.BaseHandler):
    def get(self):
        print self.get_argument('next')
        user = myTools.get_current_user(self)
        if (self.get_argument('next')):
            self.set_cookie('url', self.get_argument('next'))
        url = self.request.uri
        #self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render("login.html", user=user, url=url, login_state=login_state)

    def post(self):
        if ( myTools.is_a_attack(self) ):
            return

        self.set_header("Content-Type", "text/plain")

        email = self.get_argument('email')
        password = self.get_argument('password')

        if myTools.login(email, password):
            name = myTools.get_name_by_email(email)
            self.set_cookie('login', 'True')
            if myTools.is_user_checked(email):
                self.set_secure_cookie('name', name)
                url = self.get_cookie('url')
                self.redirect(url)
            else:
                self.set_secure_cookie('guest', name)
                self.redirect('/signup')
        else:
            self.set_cookie('login', 'False')
            self.write("Login Failed!")

