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

class SignupHandler(myTools.BaseHandler):
    def get(self):
        user = myTools.get_current_user(self)
        #if self.get_secure_cookie('guest'):
        #    user['name'] = self.get_secure_cookie('guest')
        #    user['id'] = myTools.get_id_by_name(user['name'])
        #    guest = self.get_secure_cookie('guest')
        #elif self.get_current_user():
        #    user['name'] = self.get_current_user()
        #    user['id'] = myTools.get_id_by_name(user['name'])
        login_state = self.get_cookie('login')
        print 'sign up get!'
        self.render('signup.html', user=user, url='/', login_state=login_state)

    def post(self):
        print 'post: '
        if ( myTools.is_a_attack(self) ):
            print 'is_a_attack'
            return 
      
        print 'sign up post!'
        user = {}
        user['email'] = self.get_argument('email')
        user['name'] = self.get_argument('name')
        user['password'] = self.get_argument('password')
        re_password = self.get_argument('repassword')

        print '''-
        ----- user -----
        -'''
        print user
        print 're_password: ', re_password
        print '''-
        ----- user -----
        -'''

        try:
            if self.get_argument('is_subscribed'):
                user['subscribed'] = 1
        except:
            user['subscribed'] = 0

        if user['password'] == re_password:
            if myTools.is_email_exist(user['email']) and not myTools.is_name_exist(user['name']):
                if myTools.insert_a_user(user):
                    myTools.send_check_email(user['email'])
                    print 'befor myTools.login!'
                    if myTools.login(user['email'], user['password']):
                        print 'after myTools.login!'
                        self.set_secure_cookie('guest', user['name'])
                        self.redirect('/signup')
        self.write('Signup Failed!')

