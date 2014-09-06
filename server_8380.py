#!/usr/bi/env python
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

reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options

define("port", default=8380, help="run on the given port", type=int)
# define("port", default=2357, help="run on the given port", type=int)

restrict = {}

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class Application(tornado.web.Application):
    def __init__(self):
        self.max_comm = 5000
        handlers = [
            (r'/', MainHandler),
            (r'/id/(\d+)$', NewsHandler),
            (r'/renrencallback', RenrenCallBackHandler),
            (r'/renrengettoken', RenrenGetTokenHandler),
            (r'/index', TucaoIndexHandler),
            (r'/tucao', TucaoHandler),
            (r'/tucao/(\d+)$', TucaoHandler),
            (r'/news', TucaoCommHandler),
            (r'/news/(\d+)$', TucaoCommHandler),
            (r'/blacklist', BlackListHandler),
        ]
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                ui_modules=uimodules
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if ( myTools.isInBlackList(self) ):
            return 
        self.redirect("/index")
        
    def post(self):
        if ( myTools.isInBlackList(self) ):
            return 
        # self.set_header("Content-Type", "application/json")
        raw_body = str(self.request.body)
        # print raw_body
        jsonDic = json.loads(raw_body)
        # print jsonDic 
        print jsonDic['id']
        self.write(jsonDic)
        
class RenrenCallBackHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument('code')
        print code 
        url = "https://graph.renren.com/oauth/token" +\
                    "?grant_type=authorization_code" + \
                    "&client_id=a5cd69597ccf4b369057f919928cbfce"+\
                    "&redirect_uri=http://tucao.pedestal.cn/renrencallback"+\
                    "&client_secret=ce6f56e203524cfc9c3bb61523009b6e"+\
                    "&code=" + code
        #print url
        http_client = tornado.httpclient.HTTPClient()
        response = http_client.fetch(url)
        print response.body
        jsonDic = json.loads(response.body)
        print jsonDic['access_token']
        http_client.close()

class RenrenGetTokenHandler(tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument('code')
        print token

class NewsHandler(tornado.web.RequestHandler):
    def get(self, nnid):
        if ( myTools.isInBlackList(self) ):
            return
        nid = int(nnid)
        news = myTools.get_a_news(nid)
        news['id'] = news['nid']
        news.pop('nid')
        news_json = json.dumps(news)
        self.write(news_json)

class TucaoIndexHandler(tornado.web.RequestHandler):
    def get(self):
        if ( myTools.isInBlackList(self) ):
            return
        
        try:
            page = int(self.get_argument('page'))
        except:
            page = 1 

        page_size = 20
        latest_id = myTools.get_latest_news_id()
        oldest_id = myTools.get_oldest_news_id()

        total_pages = (myTools.get_total_news_num()-1) / page_size + 1
        if page>total_pages or page<1:
            page = 1
        max_id = latest_id - (page-1)*page_size
        if page == total_pages:
            min_id = myTools.get_oldest_news_id()
        else:
            min_id = max_id - page_size + 1
        newsList = myTools.get_news_list(min_id, max_id)
        visible_pages = 10

        self.render("tucao_index.html", newsList=newsList, total_pages=total_pages, current_page=page,
                visible_pages=visible_pages)

class TucaoHandler(tornado.web.RequestHandler):
    def get(self, nnid):
        if ( myTools.isInBlackList(self) ):
            return 
        NewsDatabase.reconnect()
        nid = int(nnid)
        comm = NewsDatabase.query("""SELECT * FROM commTable WHERE id=%r ORDER
                BY level DESC, tolevel""", nid)
        # print comm
        reply = json.dumps(comm, cls=CJsonEncoder)
        # print reply
        self.write(reply)

    def post(self):
        if ( myTools.isInBlackList(self) ):
            return 
        print ("In post")
        NewsDatabase.reconnect()

        remote_ip = self.request.remote_ip
        if ( restrict.has_key( remote_ip ) ):
            if ( time.time() - restrict[remote_ip][0] < 5 ):
                self.write("less than 5 second")
                print restrict[remote_ip][0]
                print time.time()
                print "less than 5 second"
                return
            if ( restrict[remote_ip][1] > 1000 ):
                self.write("too much")
                NewsDatabase.execute(u"""INSERT blackList(ip) VALUES(%s)""", remote_ip) 
                blacklist.append(remote_ip)
                print blacklist
                print restrict[remote_ip][1]
                print "too much"
                return 
        else:
            restrict[remote_ip] = [time.time(), 0]
        
        print self.request
        raw_body = str(self.request.body)
        # print raw_body

        jsonDic = json.loads(raw_body)
        # print jsonDic
        
        nid = int(jsonDic['id'])
        content = jsonDic['content']
       
        r = r"^@(\d+):([\s\S]+)$"
        LEVEL = re.findall(r, content)
        if LEVEL:
            level = int(LEVEL[0][0])
            TOLEVEL = NewsDatabase.query("""SELECT COUNT(*) AS tolevel FROM commTable WHERE id=%r AND level=%r""", nid, level) 
            if ( int(TOLEVEL[0]['tolevel']) == 0 ):
                print "no such level"
                self.write("no such level")
                return 
            else:
                tolevel = int(TOLEVEL[0]['tolevel']) + 1
                content = LEVEL[0][1]
        else:
            tolevel = 1
            LEVEL = NewsDatabase.query("""SELECT COUNT(DISTINCT(level)) AS level FROM commTable WHERE id=%r""", nid)
            level = int(LEVEL[0]['level']) + 1

        # print content
            
        if (content == 'water'):
                NewsDatabase.execute(u"""INSERT blackList(ip) VALUES(%s)""", remote_ip) 
                blacklist.append(remote_ip)
                print blacklist
                myTools.isInBlackList(self)

        NewsDatabase.execute(u"""INSERT commTable(id, level, tolevel,
                    content) VALUES(%r, %r, %r, %s)""", nid, level, tolevel,
                    content)

        restrict[remote_ip][1] += 1
        print ("Insert comm")
        print restrict[remote_ip][1]
        
        self.write("success")

class TucaoCommHandler(tornado.web.RequestHandler):
    def get(self, nnid):
        if ( myTools.isInBlackList(self) ):
            return 
        NewsDatabase.reconnect()
        nid = int(nnid)

        news = myTools.get_a_news(nid)
        
        comm = NewsDatabase.query("""SELECT * FROM commTable WHERE id=%r ORDER
                BY level DESC, tolevel""", nid)
        latest = myTools.get_latest_news_id()
        total = myTools.get_total_news_num()
        # print comm
        self.render('TucaoComm.html', title=news['title'],\
                body=news['body'], publisher=news['publisher'],\
                date=news['date'], clean_body=news['clean_body'],\
                commList=comm, nid=nid, latest=latest, total=total)

    def post(self):
        if ( myTools.isInBlackList(self) ):
            return 
        self.application.max_comm -=1
        if self.application.max_comm <= 0:
            return
        print ("In post")
        NewsDatabase.reconnect()

        remote_ip = self.request.remote_ip
        if ( restrict.has_key( remote_ip ) ):
            if ( time.time() - restrict[remote_ip][0] < 5 ):
                self.write("less than 5 second")
                print restrict[remote_ip][0]
                print time.time()
                print "less than 5 second"
                return
            if ( restrict[remote_ip][1] > 1000 ):
                self.write("too much")
                NewsDatabase.execute(u"""INSERT blackList(ip) VALUES(%s)""", remote_ip) 
                blacklist.append(remote_ip)
                print blacklist
                print restrict[remote_ip][1]
                print "too much"
                return 
        else:
            restrict[remote_ip] = [time.time(), 0]

        raw_body = str(self.request.body)
        print self.request.remote_ip
        print raw_body

        nid = int(self.get_argument('id'))

        content = self.get_argument('content')
        r = r"^@(\d+):([\s\S]+)$"
        LEVEL = re.findall(r, content)
        if LEVEL:
            level = int(LEVEL[0][0])
            TOLEVEL = NewsDatabase.query("""SELECT COUNT(*) AS tolevel FROM commTable WHERE id=%r AND level=%r""", nid, level) 
            if ( int(TOLEVEL[0]['tolevel']) == 0 ):
                print "no such level"
                self.write("no such level")
                return 
            else:
                tolevel = int(TOLEVEL[0]['tolevel']) + 1
                content = LEVEL[0][1]
        else:
            tolevel = 1
            LEVEL = NewsDatabase.query("""SELECT COUNT(DISTINCT(level)) AS level FROM commTable WHERE id=%r""", nid)
            level = int(LEVEL[0]['level']) + 1

        # print content
            
        if (content == 'water'):
                NewsDatabase.execute(u"""INSERT blackList(ip) VALUES(%s)""", remote_ip) 
                blacklist.append(remote_ip)
                print blacklist
                myTools.isInBlackList(self)

        NewsDatabase.execute(u"""INSERT commTable(id, level, tolevel,
                    content) VALUES(%r, %r, %r, %s)""", nid, level, tolevel,
                    content)

        restrict[remote_ip][1] += 1
        restrict[remote_ip][0] = time.time()
        print ("Insert comm")
        print restrict[remote_ip][1]
        self.redirect("/news/%d" % nid)

class BlackListHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("U are in blacklist!<br>联系人人网“学生周知”")

def main():
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

def init():
    ENV_DICT['latest'] = myTools.get_latest_news_id()
    ENV_DICT['total'] = myTools.get_total_news_num()
    print ENV_DICT['total']

    BLACKLIST = NewsDatabase.query("""SELECT * FROM blackList""")
    ENV_DICT['blacklist'] = []
    for blackdict in BLACKLIST:
        ENV_DICT['blacklist'].append(blackdict['ip'])
    print ENV_DICT['blacklist']


if __name__ == "__main__":
    init()
    main()

