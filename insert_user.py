#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
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

reload(sys)
sys.setdefaultencoding('gb2312')

from tornado.options import define, options

# mail_host = "smtp.163.com"
# mail_user = "rightpeter"
# mail_pass = "15961374343"
# mail_postfix = "163.com"

if __name__=="__main__":
    user_addr = raw_input('User Email: ')
    NewsDatabase.execute("""INSERT emailTable(name, address) VALUES(%s, %s)""",
            'test', user_addr)
    subject = '学生周知邮件通知-Pedestal主页君'
    context = 'Pedestal主页君已将您加入测试列表，有任何BUG欢迎反馈' 
    if (True == myTools.send_mail([user_addr], subject, context)):
        print "success"
    else:
        print "fail"
