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
import hashlib, uuid
from config import *
from db import *
from myTools import *
import uimodules

users = NewsDatabase.query("""SELECT * from usersTable""")

for user in users:
    passwd = user['password']
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(passwd + salt).hexdigest()

    NewsDatabase.execute("""INSERT saltTable(name, salt) VALUES(%s, %s)""",
            user['name'], salt)

    NewsDatabase.execute("""UPDATE usersTable SET password=%s WHERE name=%s""",
            hashed_password, user['name'])
