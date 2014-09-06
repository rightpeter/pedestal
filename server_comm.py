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

from loginHandler import LoginHandler
from logoutHandler import LogoutHandler
from signupHandler import SignupHandler
from newsHandler import NewsHandler
from error404Handler import Error404Handler
from tucaoIndexHandler import TucaoIndexHandler
from aboutHandler import AboutHandler
from projectHandler import ProjectHandler
from tucaoCommHandler import TucaoCommHandler
from homeHandler import HomeHandler
from profileHandler import ProfileHandler
from languagesActivitiesHandler import LanguagesActivitiesHandler
from indoorHandler import IndoorHandler
from indoorMapHandler import IndoorMapHandler
from tucaoHandler import TucaoHandler

reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)
# define("port", default=2357, help="run on the given port", type=int)

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
        #self.max_comm = 5000
        handlers = [
            (r'/', MainHandler),
            # API -----------------
            (r'/api', APIHandler),
            (r'/api/follow', FllwHandler),
            (r'/api/subscribed', SbscHandler),
            (r'/api/check', CheckHandler),
            (r'/api/cgname', ChangeNameHandler),
            (r'/api/cgpasswd', ChangePasswdHandler),
            (r'/api/cgavatar', ChangeAvatarHandler),
            (r'/api/login', APILoginHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/signup', SignupHandler),
            (r'/id/(\d+)$', NewsHandler),
            (r'/renrencallback', RenrenCallBackHandler),
            (r'/renrengettoken', RenrenGetTokenHandler),
            
            (r'/404', Error404Handler),
            (r'/index', TucaoIndexHandler),
            (r'/about', AboutHandler),
            (r'/project', ProjectHandler),
            #(r'/tucao', TucaoHandler),
            #(r'/tucao/(\d+)$', TucaoHandler),
            (r'/news', TucaoCommHandler),
            (r'/news/(\d+)$', TucaoCommHandler),
            (r'/home/(\d+)$', HomeHandler),
            (r'/profile', ProfileHandler),
            (r'/languagesactivities', LanguagesActivitiesHandler),
            (r'/app/indoor$', IndoorHandler),
            (r'/app/indoor/map$', IndoorMapHandler),
            #(r'/blacklist', BlackListHandler),
        ]
        settings = { 
                "template_path": os.path.join(os.path.dirname(__file__), "templates"),
                "static_path": os.path.join(os.path.dirname(__file__), "static"),
                "ui_modules": uimodules,
                "cookie_secret": "#De1rFq@oyW^!kc3MI@74LY*^TPG6J8fkiG@xidDBF",
                "login_url": "/login",
                "xsrf_cookies": True,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

#class IndoorHandler(BaseHandler):
#    @tornado.web.authenticated
#    def get(self):
#        user = myTools.get_current_user(self)
#        url = self.request.uri
#        self.set_cookie('url', url)
#        login_state = self.get_cookie('login')
#        self.render('WorldMap.html', user=user, url=url, login_state=login_state)

class MainHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        slides = [{}, {}, {}, {}]
        slides[0]['image'] = "tucao_slide.jpg"
        slides[0]['name'] = "周知吐槽"
        slides[0]['descript'] = "尽情地为自己呐喊"
        slides[0]['href'] = "/index"
        slides[0]['button'] = "开始吐槽"

        slides[1]['image'] = "english_month.jpg"
        slides[1]['name'] = "这只是一个大标题"
        slides[1]['descript'] = "用来测试轮播插件这个复杂的东西"
        slides[1]['href'] = "/languagesactivities"
        slides[1]['button'] = "关注语言与思维实训基地"

        slides[2]['image'] = "pedestal.jpg"
        slides[2]['name'] = "周知吐槽"
        slides[2]['descript'] = "尽情地为自己呐喊"
        slides[2]['href'] = "/about"
        slides[2]['button'] = "关于我们"
       
        slides[3]['image'] = "pedestal_welcome.jpg"
        slides[3]['name'] = "这只是一个大标题"
        slides[3]['descript'] = "用来测试轮播插件这个复杂的东西"
        slides[3]['href'] = "/signup"
        slides[3]['button'] = "加入我们"

        
        user = myTools.get_current_user(self)
        self.set_cookie("url", self.request.uri)
        url = self.request.uri

        login_state = self.get_cookie('login')
        self.render("index.html", slides=slides, user=user, url=url,
                login_state=login_state)
        
class APIHandler(BaseHandler):
    def get(self):
        jsonDict = {}
        api_type = self.get_argument('type')
        value = self.get_argument('value')
        call_back = self.get_argument('callback')
        jsonDict['value'] = value
        if api_type == 'EMAIL':
            jsonDict['type'] = "EMAIL"
            if myTools.is_email_exist(value):
                jsonDict['status'] = "UNIQUE"
            else:
                jsonDict['status'] = "REPEATED"

        if api_type == 'NAME':
            jsonDict['type'] = "NAME"
            if not myTools.is_name_exist(value): 
                jsonDict['status'] = "UNIQUE"
            else:
                jsonDict['status'] = "REPEATED"

        encoded_json = json.dumps(jsonDict)
        call_back_json = '%s(%s)' % (call_back, encoded_json)
        self.write(call_back_json)

class APILoginHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(1001, 'Login Failed')

class FllwHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        pid = int(self.get_argument('pid'))
        fname = self.get_current_user()
        if myTools.follow(pid, fname):
            self.write("Succeed Following!")
        else:
            self.write("Followed Error!")
        
class SbscHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        subscribed = int(self.get_argument('subscribed'))
        name = self.get_current_user()
        if myTools.subscribe(name, subscribed):
            self.write("Succeed Subscribing!")
        else:
            self.write("Subscribed Error!")

class CheckHandler(BaseHandler):
    def get(self):
        try:
            code = self.get_argument('code')
            email = self.get_argument('email') 
            name = myTools.get_name_by_email(email)
            if myTools.check_email(email, code):
                self.set_secure_cookie('name', name)
                self.redirect('/signup')
            else:
                self.write('Checked Failed!')
        except: 
            name = self.get_argument('name')
            email = myTools.get_email_by_name(name)
            myTools.send_check_email(email)


class ChangeNameHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = self.get_current_user() 
        try:
            new_name = self.get_argument('new_name')
        except:
            new_name = ''

        self.clear_cookie('name')
        self.clear_cookie('guest')
        self.clear_cookie('login')
        if myTools.change_name(name, new_name):
            print 'success'
            self.write('Name changed!')
        else:
            print 'fail'
            self.write('Changing Name Failing!')
            
    
class ChangePasswdHandler(BaseHandler):
    # @tornado.web.authenticated
    # def get(self):
    #     name = self.get_current_user()
    #     email = myTools.get_email_by_name(name)
    #     passwd = self.get_argument('passwd')
    #     new_passwd = self.get_argument('new_passwd')
    #     re_new_passwd = self.get_argument('re_new_passwd')
    #     
    #     if myTools.change_passwd(email, passwd, new_passwd, re_new_passwd):
    #         self.write('Passwd Changed!')
    #     else:
    #         self.write('Changing Passwd Fail!')

    @tornado.web.authenticated
    def post(self):
        name = self.get_current_user()
        email = myTools.get_email_by_name(name)
        passwd = self.get_argument('passwd')
        new_passwd = self.get_argument('new_passwd')
        re_new_passwd = self.get_argument('re_new_passwd')
        
        if myTools.change_passwd(email, passwd, new_passwd, re_new_passwd):
            self.write('Passwd Changed!')
        else:
            self.write('Changing Passwd Fail!')

class ChangeAvatarHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = self.get_current_user()
        email = myTools.get_email_by_name(name)
        uid = myTools.get_id_by_name(name)
        
        if self.request.files:
            try:
                avatar = self.request.files['avatar'][0]
                filename = avatar['filename']

                re_ext = '([^\s]+(\.(?i)(jpg|png|gif|bmp))$)'
                avatar_ext = re.findall(re_ext, filename)[0][1]
                filename = '%s%s' % (uid, avatar_ext)
                avatar_file = '%s%s' % (avatar_path, filename)
                image = open(avatar_file, 'w')
                print 'success to open: ' + avatar_file
                image.write(avatar['body'])
                image.close()
                NewsDatabase.execute("""UPDATE usersTable SET ext=%s WHERE
                        email=%s""", avatar_ext, email)
                print 'avatar success'
                print '/home/%s', uid
                self.redirect('/home/%s' % uid)
            except:
                print 'avatar fail'
                self.write('Changing Avatar Failing!')


class RenrenCallBackHandler(BaseHandler):
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

class RenrenGetTokenHandler(BaseHandler):
    def get(self):
        token = self.get_argument('code')
        print token

class BlackListHandler(BaseHandler):
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
    ENV_DICT['restrict'] = {}
    for blackdict in BLACKLIST:
        ENV_DICT['blacklist'].append(blackdict['ip'])
    print ENV_DICT['blacklist']


if __name__ == "__main__":
    init()
    main()


