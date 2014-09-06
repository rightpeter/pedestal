#!/usrebin/env python
#-*- coding: utf-8 -*-

import MySQLdb
import sys
import os
import re
import time
import json
import tornado.web
import tornado.ioloop
# tornado 3.x nolonger have this. use torndb
import tornado.database
#import torndb
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
from testMyTools import *

reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options

# define("port", default=2357, help="run on the given port", type=int)
define("port", default=2358, help="run on the given port", type=int)

NewsDatabase.reconnect()
home_page = "http://210.30.97.149:2358"
local_page = "210.30.97.149"
ali_page = "115.28.2.165"

mail_host = "smtp.163.com"
mail_user = "pedestal_peter"
mail_pass = "15961374343"
mail_postfix = "163.com"

def email_notice(pre_latest, new_latest): 
    if pre_latest < new_latest:
        #NewsDatabase.reconnect()
        #users = NewsDatabase.query("""SELECT name, address FROM emailTable""")
        #print users

        print new_latest
        news = testMyTools.get_a_news(new_latest)

        subject = u''.join([
            news['title'],
            ' - ',
            news['publisher']])
            
        subject = "这是测试邮件：" + subject 
        context = """<a
            href="http://tucao.pedestal.cn:2358/tucao/comm/%s">%s</a><br>"""%(new_latest,
                subject) +\
                """<div align="LEFT" style="width:600px;">""" +\
                news['body'] +\
                "</div>"

        for i in range(pre_latest+1, new_latest):
            print 'tmp_news: ', i
            tmp_news = testMyTools.get_a_news(i) 

            if tmp_news:
                tmpTitle = u''.join([
                    tmp_news['title'],
                    ' - ',
                    tmp_news['publisher']])

                context += u"""您可能错过了：<a href="http://210.30.97.149:2358/tucao/comm/%s">%s</a><br>
                    """ % (i, tmpTitle)
           
        users = [{'name':'peter', 'address':'327888145@qq.com'}, {'name':'peter', 'address':'rightpeter.lu@gmail.com'}]
        for user in users:
            print user['name'], ':', user['address']
            if (True == testMyTools.send_mail([user['address']], subject, context)):
                print "success to ", user['name']
            else:
                print "fail to ", user['name']
        return True
    else:
        return False 


def update_latest():
    maxid = testMyTools.get_latest_news_id()
    maxnid = testMyTools.get_latest_news_nid()
    latest = json.loads(testMyTools.get_json(ali_page, "/latest"))['id']
    print datetime.datetime.now(), ':', maxnid, ',', latest

    for i in range(maxnid+1, latest+1):
        testMyTools.add_news(i)
    
    latest = testMyTools.get_latest_news_id()
    print latest
    email_notice(maxid, latest)
    return latest


if __name__ == "__main__":
    url = "/latest"
    while True:
        update_latest()
        time.sleep(15)

    #while True:
    #    print 'xixi'
    #    raw_news = get_page_data(url)
    #    jsonDic = json.loads(raw_news)

    #    new_latest = jsonDic['id'] 
    #    try:
    #        f = open('env_dict.pickle', 'rb')
    #        env_dict = pickle.load(f)
    #        f.close()
    #    except:
    #        env_dict = {}
    #        env_dict['latest'] = new_latest-5
    #        f = open('env_dict.pickle', 'wb')
    #        pickle.dump(env_dict, f)
    #        f.close()
    #    pre_latest = env_dict['latest']

    #    if update_news(pre_latest, new_latest):
    #        env_dict['latest'] = new_latest
    #        f = open('env_dict.pickle', 'wb')
    #        pickle.dump(env_dict, f)
    #        print 'update: %s %s' % (pre_latest, new_latest)
    #    else:
    #        print 'nothing'
    #        
    #    time.sleep(15)
