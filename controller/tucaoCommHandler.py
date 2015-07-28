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

class TucaoCommHandler(myTools.BaseHandler):
    def get(self, nnid):
        NewsDatabase.reconnect()
        nid = int(nnid)

        max_id = myTools.get_latest_news_id()
        min_id = max_id-5
        newsList = myTools.get_news_list(min_id, max_id)
        for news in newsList:
            news['title'] = news['title'][:15] + '...'

        news = myTools.get_a_news(nid)

        news['body'] = news['body'].replace('href="/Attachments/file', 'href="http://ssdut.dlut.edu.cn/Attachments/file')
        news['body'] = news['body'].replace('src="/Attachments/image', 'src="http://ssdut.dlut.edu.cn/Attachments/image')

        comm = NewsDatabase.query("""SELECT * FROM commTable WHERE id=%r ORDER
                BY level DESC, tolevel""", nid)
        latest = myTools.get_latest_news_id()
        total = myTools.get_total_news_num()
        # print comm

        user = myTools.get_current_user(self)
        self.set_cookie("url", self.request.uri)
        url = self.request.uri
        login_state = self.get_cookie('login')
        self.render('tucao_news.html', newsList=newsList, title=news['title'],\
                body=news['body'], publisher=news['publisher'],\
                date=news['date'], clean_body=news['clean_body'],\
                commList=comm, nid=nid, latest=latest, total=total, 
                user=user, url=url, login_state=login_state)

        #self.render('TucaoComm.html', title=news['title'],\
        #        body=news['body'], publisher=news['publisher'],\
        #        date=news['date'], clean_body=news['clean_body'],\
        #        commList=comm, nid=nid, latest=latest, total=total, 
        #        user=user, url=url, login_state=login_state)

    def post(self):
        if ( myTools.is_a_attack(self) ):
            self.redirect("/blacklist")
            return 

        print ("In post")
        NewsDatabase.reconnect()

        raw_body = str(self.request.body)
        print self.request.remote_ip
        print raw_body

        nid = int(self.get_argument('id'))
        nnid = NewsDatabase.query("""SELECT nid from newsTable WHERE id=%s""",
                nid)[0]['nid']
        nnid = int(nnid)
        print nnid

        try:
            level = int(self.get_argument('level'))
        except:
            level = 0
        content = self.get_argument('content')

        if level==0:
            tolevel = 1
            LEVEL = NewsDatabase.query("""SELECT COUNT(DISTINCT(level)) AS level FROM commTable WHERE id=%r""", nid)
            level = int(LEVEL[0]['level']) + 1
        else:
            TOLEVEL = NewsDatabase.query("""SELECT COUNT(*) AS tolevel FROM commTable WHERE id=%r AND level=%r""", nid, level) 
            if ( int(TOLEVEL[0]['tolevel']) == 0 ):
                print "no such level"
                self.write("no such level")
                return 
            else:
                tolevel = int(TOLEVEL[0]['tolevel']) + 1
       

        #r = r"^@(\d+):([\s\S]+)$"
        #LEVEL = re.findall(r, content)
        #if LEVEL:
        #    level = int(LEVEL[0][0])
        #    TOLEVEL = NewsDatabase.query("""SELECT COUNT(*) AS tolevel FROM commTable WHERE id=%r AND level=%r""", nid, level) 
        #    if ( int(TOLEVEL[0]['tolevel']) == 0 ):
        #        print "no such level"
        #        self.write("no such level")
        #        return 
        #    else:
        #        tolevel = int(TOLEVEL[0]['tolevel']) + 1
        #        content = LEVEL[0][1]
        #else:
        #    tolevel = 1
        #    LEVEL = NewsDatabase.query("""SELECT COUNT(DISTINCT(level)) AS level FROM commTable WHERE id=%r""", nid)
        #    level = int(LEVEL[0]['level']) + 1

        # print content
            
        if (content == 'water'):
                NewsDatabase.execute(u"""INSERT blackList(ip) VALUES(%s)""", remote_ip) 
                ENV_DIC['blacklist'].append(remote_ip)
                myTools.is_a_attack(self)

        NewsDatabase.execute(u"""INSERT commTable(id, level, tolevel,
                    content, nid) VALUES(%r, %r, %r, %s, %s)""", nid, level, tolevel,
                    content, nnid)

        myTools.post_once(self)
        self.redirect('/news/%d' % nid)

