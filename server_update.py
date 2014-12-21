#!/usrebin/env python
#-*- coding: utf-8 -*-

import MySQLdb
import sys
import os
import re
import time
import json
import tornado
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
from model import *
from config import *
import util.myTools as myTools

reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options

# define("port", default=2357, help="run on the given port", type=int)
# define("port", default=2358, help="run on the given port", type=int)

mail_host = "smtp.163.com"
mail_user = "pedestal_peter"
mail_pass = "15961374343"
mail_postfix = "163.com"

def email_notice(pre_latest, new_latest): 
    if pre_latest < new_latest:
        NewsDatabase.reconnect()
        users = NewsDatabase.query("""SELECT name, email FROM usersTable WHERE
                subscribed=1""")
        print users

        print new_latest
        news = myTools.get_a_news(new_latest)

        news['body'] = news['body'].replace('href="/Attachments/file', 'href="http://ssdut.dlut.edu.cn/Attachments/file')
        news['body'] = news['body'].replace('src="/Attachments/image', 'src="http://ssdut.dlut.edu.cn/Attachments/image')
        
        subject = u''.join([
            news['title'],
            ' - ',
            news['publisher']])
            
        context = """<a
            href="%s/news/%s">%s</a><br>"""%(HOME_PAGE, new_latest,
                subject) +\
                """<div align="LEFT" style="width:600px;">""" +\
                news['body'] +\
                "</div>"

        for i in range(pre_latest+1, new_latest):
            print 'tmp_news: ', i
            tmp_news = myTools.get_a_news(i) 

            if tmp_news:
                tmpTitle = u''.join([
                    tmp_news['title'],
                    ' - ',
                    tmp_news['publisher']])

                context += u"""您可能错过了：<a 
                    href="http://%s/news/%s">%s</a><br>
                    """ % (HOME_PAGE, i, tmpTitle)
           
        #users = [{'name':'peter', 'address':'327888145@qq.com'}, {'name':'peter', 'address':'rightpeter.lu@gmail.com'}]
        tmp_subject = subject
        for user in users:
            if re.findall(re_email, user['email'])[0][1] == 'qq':
                subject = '您好' + user['name']
            else:
                subject = tmp_subject
        
            print user['name'], ':', user['email']
            if (True == myTools.send_mail([user['email']], subject, context)):
                print "success to ", user['name']
            else:
                print "fail to ", user['name']
        return True
    else:
        return False 


def update_latest():
    maxid = myTools.get_latest_news_id()
    maxnid = myTools.get_latest_news_nid()
    latest = json.loads(myTools.get_json(ali_page, "/latest"))['id']
    print datetime.datetime.now(), ':', maxnid, ',', latest

    for i in range(maxnid+1, latest+1):
        myTools.add_news(i)
    
    latest = myTools.get_latest_news_id()
    print latest
    email_notice(maxid, latest)
    return latest


if __name__ == "__main__":
    url = "/latest"
    while True:
        update_latest()
        time.sleep(UPDATE_INTERVAL)
