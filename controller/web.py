#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
from config import *
from model import *
import util.myTools as myTools
import util.uimodules as uimodules

BaseHandler = myTools.BaseHandler

class LoginHandler(BaseHandler):
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

class LogoutHandler(BaseHandler):
    def get(self):
        url = self.get_cookie('url')
        self.clear_cookie('name')
        self.clear_cookie('guest')
        self.clear_cookie('login')
        self.redirect(url)

class SignupHandler(BaseHandler):
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
        self.render('signup.html', user=user, url='/', login_state=login_state)

    def post(self):
        if ( myTools.is_a_attack(self) ):
            return 
      
        user = {}
        user['email'] = self.get_argument('email')
        user['name'] = self.get_argument('name')
        user['password'] = self.get_argument('password')
        re_password = self.get_argument('repassword')
        try:
            if self.get_argument('is_subscribed'):
                user['subscribed'] = 1
        except:
            user['subscribed'] = 0

        if user['password'] == re_password:
            if myTools.is_email_exist(user['email']) and not myTools.is_name_exist(user['name']):
                if myTools.insert_a_user(user):
                    myTools.send_check_email(user['email'])
                    if myTools.login(user['email'], user['password']):
                        self.set_secure_cookie('guest', user['name'])
                        self.redirect('/signup')
        self.write('Signup Failed!')

class NewsHandler(BaseHandler):
    def get(self, nnid):
        nid = int(nnid)
        news = myTools.get_a_news(nid)
        news['id'] = news['nid']
        news.pop('nid')
        news_json = json.dumps(news)
        self.write(news_json)

class Error404Handler(BaseHandler):
    def get(self):
        user = myTools.get_current_user(self)
        url = self.request.uri
        self.render('404.html', user=user, url=url, login_state='Not')

class TucaoIndexHandler(BaseHandler):
    def get(self):
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
        for news in newsList:
            news['clean_body'] = news['clean_body'][:300] + '......'
        visible_pages = 10

        user = myTools.get_current_user(self)
        self.set_cookie("url", self.request.uri)
        url = self.request.uri
        login_state = self.get_cookie('login')
        self.render("news_list.html", newsList=newsList,
                total_pages=total_pages, current_page=page,
                visible_pages=visible_pages, user=user, url=url,
                login_state=login_state)
        #self.render("tucao_index.html", newsList=newsList, total_pages=total_pages, current_page=page,
        #        visible_pages=visible_pages, user=user, url=url,
        #        login_state=login_state)

class TucaoHandler(BaseHandler):
    def get(self, nnid):
        if ( myTools.is_a_attack(self) ):
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
        if ( myTools.is_a_attack(self) ):
            return 

        print ("In post")
        NewsDatabase.reconnect()

        remote_ip = self.request.remote_ip
        if ( restrict.has_key(remote_ip) ):
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
                myTools.is_a_attack(self)

        NewsDatabase.execute(u"""INSERT commTable(id, level, tolevel,
                    content) VALUES(%r, %r, %r, %s)""", nid, level, tolevel,
                    content)

        restrict[remote_ip][1] += 1
        print ("Insert comm")
        print restrict[remote_ip][1]
        
        self.write("success")


class TucaoCommHandler(BaseHandler):
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

class AboutHandler(BaseHandler):
    def get(self):
        user = myTools.get_current_user(self) 
        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('about.html', user=user, url=url, login_state=login_state)

class ProjectHandler(BaseHandler):
    def get(self):
        user = myTools.get_current_user(self)
        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('laboratory.html', user=user, url=url, login_state=login_state)

class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, home_id):
        home_name = myTools.get_name_by_id(home_id)
        user = myTools.get_current_user(self)
        avatar_ext = myTools.get_avatar_ext_by_id(home_id)
        if avatar_ext:
            avatar_file = '%s%s' % (home_id, avatar_ext)
            # print 'avatar_file: ', avatar_file 
            if not os.path.exists(avatar_path + avatar_file):
                avatar_file = 'default.jpg'
        else:
            avatar_file = 'default.jpg'

        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('home.html', home_name=home_name, user=user,
                avatar_file=avatar_file, url=url,
                login_state=login_state)

class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = myTools.get_current_user(self)
        user_name = self.get_current_user()
        user_detail = myTools.get_user_by_name(user_name)
        url = self.request.uri
        self.set_cookie('url', url)
        login_state = self.get_cookie('login')
        self.render('profile.html', user_detail=user_detail, user=user, url=url,
                login_state=login_state)

class LanguagesActivitiesHandler(BaseHandler):
    def get(self):
        user = myTools.get_current_user(self)
        self.set_cookie("url", self.request.uri)
        url = self.request.uri

        login_state = self.get_cookie('login')
        
        self.render('languages_activities.html', user=user, url=url,
                login_state=login_state)


