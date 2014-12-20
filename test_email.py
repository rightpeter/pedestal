#!/usr/bin/env python

import MySQLdb
import hashlib, uuid
import string
import sys
import os
from os import urandom
from random import choice
import re
import time
import json
import tornado.web
import tornado.ioloop
import torndb
import math
import httplib
import json
import pickle
import datetime
import threading
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from db import *
from config import *
from myTools import *

NewsDatabase.reconnect()
users = NewsDatabase.query("""SELECT name, email FROM usersTable WHERE
        subscribed=1""")
print users


subject = u'hehe'
    
context = 'hehe'

users = [{'name':'peter', 'email':'327888145@qq.com'}, {'name':'peter', 'email':'rightpeter.lu@gmail.com'}]
for user in users:
    print user['name'], ':', user['email']
    
    if (True == myTools.send_mail([user['email']], subject, context)):
        print "success to ", user['name']
    else:
        print "fail to ", user['name']




