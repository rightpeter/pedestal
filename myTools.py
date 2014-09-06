#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("name")

    def get_login_url(self):
        return "/login"

class myTools:
    @classmethod
    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    @classmethod
    def generate_password(self, passwd_length, passwd_seed):
        passwd = []
        while len(passwd) < passwd_length:
            passwd.append(choice(passwd_seed))
        return ''.join(passwd)

    @classmethod
    def get_json(self, domain, url):
        try:
            httpClient = httplib.HTTPConnection(domain, 8000, timeout=2000)
            httpClient.request('GET', url) 

            response = httpClient.getresponse()
            # print response.status
            response.reason
            return response.read()
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()
        #return raw_news

    @classmethod
    def get_latest_news_id(self):
        maxid = NewsDatabase.query("""SELECT MAX(id) AS mid FROM newsTable""")
        if maxid[0]['mid']:
            maxid = int(maxid[0]['mid'])
        else:
            maxid = 0 
        return maxid       

    @classmethod
    def get_latest_news_nid(self):
        maxnid = NewsDatabase.query("""SELECT MAX(nid) AS mnid FROM newsTable""")
        if maxnid[0]['mnid']:
            maxnid = int(maxnid[0]['mnid'])
        else:
            maxnid = 0
        return maxnid

    @classmethod
    def get_total_news_num(self):
        total = NewsDatabase.query("""SELECT COUNT(id) AS total FROM newsTable""")
        total = int(total[0]['total'])
        return total

    @classmethod
    def get_oldest_news_id(self):
        minid = NewsDatabase.query("""SELECT MIN(id) AS mid FROM newsTable""")
        if minid[0]['mid']:
            minid = int(minid[0]['mid'])
        else:
            minid = 0
        return minid

    @classmethod
    def get_a_news(self, nid):
        news = NewsDatabase.query("""SELECT * FROM newsTable WHERE id=%s""",
                nid)
        if len(news):
            return news[0]
        else:
            return {} 


    @classmethod
    def get_news_list(self, min_id, max_id):
        newsList = NewsDatabase.query("""SELECT * FROM newsTable WHERE id<=%s
                and id>=%s ORDER BY id DESC""", max_id, min_id)
        if len(newsList):
            return newsList
        else:
            return {}

    @classmethod
    def get_password_by_email(self, email):
        password = NewsDatabase.query("""SELECT password FROM usersTable WHERE
            email=%s""", email)[0]['password']
        return password

    @classmethod
    def get_email_by_name(self, name):
        user_email = NewsDatabase.query("""SELECT email FROM usersTable WHERE
                name=%s""", name) 
        if len(user_email):
            user_email = user_email[0]['email']
        else:
            user_email = ''
        return user_email

    @classmethod
    def get_id_by_name(self, name):
        user_id = NewsDatabase.query("""SELECT id FROM usersTable WHERE
                name=%s""", name)
        if len(user_id):
            user_id = int(user_id[0]['id'])
        else:
            user_id = -1 
        return user_id

    @classmethod
    def get_name_by_email(self, email):
        name = NewsDatabase.query("""SELECT name FROM usersTable WHERE
                email=%s""", email)
        if len(name):
            name = name[0]['name']
        else:
            name = ''
        return name

    @classmethod
    def get_name_by_id(self, user_id):
        name = NewsDatabase.query("""SELECT name FROM usersTable WHERE
                id=%s""", user_id)
        if len(name):
            name = name[0]['name']
        else:
            name = ''
        return name

    @classmethod
    def get_user_by_id(self, user_id):
        user = NewsDatabase.query("""SELECT id, name, email FROM usersTable
                WHERE id=%s""", user_id)
        if len(user):
            user = user[0]
        else:
            user = ''
        return user

    @classmethod
    def get_user_by_name(self, user_name):
        user = NewsDatabase.query("""SELECT id, name, email FROM usersTable
                WHERE name=%s""", user_name)
        if len(user):
            user = user[0]
        else:
            user = ''
        return user

    @classmethod
    def get_salt_by_email(self, email):
        salt = NewsDatabase.query("""SELECT salt FROM saltTable WHERE
            email=%s""", email)
        if len(salt):
            salt = salt[0]['salt']
        else:
            salt = ''
        return salt

    @classmethod
    def get_avatar_ext_by_email(self, email):
        ext = NewsDatabase.query("""SELECT ext FROM usersTable WHERE
            email=%s""", email)
        if len(ext):
            ext = ext[0]['ext']
        else:
            ext = ''
        return ext 

    @classmethod
    def get_avatar_ext_by_id(self, id):
        ext = NewsDatabase.query("""SELECT ext FROM usersTable WHERE
            id=%s""", id)
        if len(ext):
            ext = ext[0]['ext']
        else:
            ext = ''
        return ext 

    @classmethod
    def send_mail(self, to_email, sub, context):
        #if re.findall(re_email, to_email)[0][1] == 'qq':
        #    poster = 'qq'
        #else:
        #    poster = '163'
        poster = '163'

        me = mail_poster[poster]['user'] + "<" + mail_poster[poster]['user'] + "@" + mail_poster[poster]['postfix'] + ">"
        msg = MIMEText(context, 'html', 'utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = to_email[0]
        #print msg
        print mail_poster[poster]
        #try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_poster[poster]['host'])
        send_smtp.login(mail_poster[poster]['user'], mail_poster[poster]['pass'])
        send_smtp.sendmail(me, to_email, msg.as_string())
        send_smtp.close()
        return True
        #except (Exception, e):
        #    print(str(e))
        #    return False

    @classmethod
    def update_check(self, email, code):
        record = NewsDatabase.query("""SELECT * FROM checkTable WHERE
                email=%s""", email)
        if len(record):
            NewsDatabase.execute("""UPDATE checkTable SET code=%s,
                    check_time=%s, checked=%s WHERE email=%s""", code,
                    self.now()[0], '0', email)
        else:
            NewsDatabase.execute("""INSERT checkTable(email, code, checked) VALUES(%s,
                    %s, %s)""", email, code, '0')

    @classmethod
    def send_check_email(self, email):
        passwd_seed = string.digits + string.ascii_letters + string.punctuation
        code = self.generate_password(30, passwd_seed)
        name = myTools.get_name_by_email(email)
        self.update_check(email, code)
        subject = '%s您好' % name
        
        code = tornado.escape.url_escape(code)
        context = 'http://www.pedestal.cn/api/check?email=%s&code=%s' % (email,
                code)
        print context

        name = self.get_name_by_email(email)
        if (True == myTools.send_mail(email, subject, context)):
            print 'success to ', name
            return True
        else:
            print 'fail to ', name
            return False

    @classmethod
    def check_email(self, email, code):
        ccode = NewsDatabase.query("""SELECT code, checked FROM checkTable WHERE
            email=%s""", email)
        if len(ccode):
            checked = ccode[0]['checked']
            ccode = ccode[0]['code']
            print 'code: ', code
            print 'ccode: ', ccode
            if ccode == code and checked == 0: 
                NewsDatabase.execute("""UPDATE usersTable SET checked=1 WHERE
                        email=%s""", email)
                NewsDatabase.execute("""UPDATE checkTable SET checked=1 WHERE
                        email=%s""", email)
                return True
        return False

    @classmethod
    def add_news(self, id): 
        url = "/id/%s" % id
        raw_news = self.get_json(ali_page, url)

        if raw_news:
            json_dic = json.loads(raw_news)

            print self.now(), ':', id, 'insert'
            NewsDatabase.execute("""INSERT newsTable
                (nid,publisher,sha1,date,title,source,
                link,source_link,clean_body,body)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" \
                ,json_dic['id'],\
                 json_dic['publisher'],\
                 json_dic['sha1'],\
                 json_dic['date'],\
                 json_dic['title'],\
                 json_dic['source'],\
                 json_dic['link'],\
                 json_dic['source_link'],\
                 json_dic['clean_body'],\
                 json_dic['body'])
            return True
        else:
            print self.now(), ':', id, 'nothing'
            #NewsDatabase.execute("""INSERT newsTable(nid) VALUES(%s)""", 9999)
            return False


    @classmethod
    def is_a_attack(self, httprequest):
        ip = httprequest.request.remote_ip

        if ( ip in ENV_DICT['blacklist'] ):
            print "In black list"
            return True
       
        if ( ip in ENV_DICT['restrict'] ):
            if ( time.time() - ENV_DICT['restrict'][ip][0] < 5 ):
                httprequest.write("less than 5 second")
                print ENV_DICT['restrict'][ip][0]
                print time.time()
                print "less than 5 second"
                httprequest.write("less than 5 second")
                return True
            if ( ENV_DICT['restrict'][ip][1] > 1000 ):
                httprequest.write("too much")
                NewsDatabase.execute(u"""INSERT blackList(ip) VALUES(%s)""", ip) 
                ENV_DICT['blacklist'].append(ip)
                print ENV_DICT['restrict'][ip][1]
                print "too much"
                httprequest.write("no attack!")
                return True
        else:
            ENV_DICT['restrict'][ip] = [0, 0]
        
        
        print "-----------------------------one request-----------------------------"
        print "method: %s" % httprequest.request.method
        print "uri: %s" % httprequest.request.uri
        print "remote_ip: %s" % httprequest.request.remote_ip
        print "body: %s" % httprequest.request.body
        print "time: %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print "-----------------------------one request-----------------------------"
        return False

    @classmethod
    def post_once(self, httprequest):
        ip = httprequest.request.remote_ip
        ENV_DICT['restrict'][ip][1] += 1
        ENV_DICT['restrict'][ip][0] = time.time()
        print ("Insert comm")
        print ENV_DICT['restrict'][ip][1]
       

    @classmethod
    def is_email_exist(self, email):
        re_email = r'^([[a-zA-Z0-9]+[_|\_|\.]?]*[a-zA-Z0-9]+)@([[a-zA-Z0-9]+[_|\_|\.]?]*[a-zA-Z0-9]+)\.[a-zA-Z]{2,4}$'
        isEmail = bool(re.match(re_email, email, re.VERBOSE))
        email_sql = NewsDatabase.query("""SELECT email FROM usersTable WHERE
            email=%s""", email)
        if len(email_sql) or not isEmail:
            return False
        else:
            return True

    @classmethod
    def is_name_exist(self, name):
        name_sql = NewsDatabase.query("""SELECT name FROM usersTable WHERE
            name=%s""", name)
        if len(name_sql):
            return True 
        else:
            return False 

    @classmethod
    def is_user_checked(self, email):
        checked = NewsDatabase.query("""SELECT checked FROM usersTable WHERE
            email=%s""", email)
        if len(checked):
            return checked[0]['checked']
        else:
            return False 

    @classmethod
    def insert_a_user(self, user):
        passwd = user['password']
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(passwd + salt).hexdigest()

        try:
            user['subscribed'] = 1;
            NewsDatabase.execute("""INSERT usersTable(email, name, password,
                subscribed) VALUES(%s, %s, %s, %s)""", user['email'], user['name'],
                hashed_password, user['subscribed']) 
            NewsDatabase.execute("""INSERT saltTable(email, salt) VALUES(%s, %s)""",
                user['email'], salt)
            return True
        except:
            return False

    @classmethod
    def get_current_user(self, request):
        user = {}
        name = request.get_current_user()
        if name:
            user['vip'] = {}
            user['vip']['name'] = name
            user['vip']['id'] = myTools.get_id_by_name(name)
        name = request.get_secure_cookie('guest')
        if name:
            user['guest'] = {}
            user['guest']['name'] = name
            user['guest']['id']  = myTools.get_id_by_name(name)
        return user
        
    @classmethod
    def login(self, email, password):
        if not self.is_email_exist(email):
            check = self.get_password_by_email(email) 
            salt = myTools.get_salt_by_email(email)
            hashed_password = hashlib.sha512(password+salt).hexdigest()
            if hashed_password == check:
                NewsDatabase.execute("""UPDATE usersTable SET last_login=%s
                        WHERE email=%s""",
                        self.now()[0],
                        email)
                name = myTools.get_name_by_email(email)
                print "email: ", email
                print "name", name
                print "password: ", password
                return True
        return False
        
    @classmethod
    def follow(self, pid, fname):
        fid = NewsDatabase.query("""SELECT id FROM usersTable WHERE name=%s""",
                fname)
        pname = NewsDatabase.query("""SELECT name FROM usersTable WHERE
                id=%s""", pid)
        if len(fid) and len(pname):
            fid = fid[0]['id']
            record = NewsDatabase.query("""SELECT id FROM fllwTable WHERE pid=%s
                and fid=%s""", pid, fid)
            if not len(record): 
                NewsDatabase.execute("""INSERT fllwTable(pid, fid) VALUES(%s, %s)""", pid, fid)
                return True
        return False

    @classmethod
    def subscribe(self, name, subscribed):
        user = NewsDatabase.query("""SELECT id, subscribed FROM usersTale WHERE
            name=%s""", name)

        if len(user):
            user = user[0]
            if int(user['subscribed']) != subscribed:
                NewsDatabase.execute("""UPDATE usersTable SET subscribed=%s
                        WHERE name=%s""", subscribed, name)
                return True
        return False

    @classmethod
    def change_passwd(self, email, passwd, new_passwd, re_new_passwd):
        if myTools.login(email, passwd) and new_passwd==re_new_passwd:
            name = self.get_name_by_email(email)
            passwd = new_passwd
            salt = uuid.uuid4().hex
            hashed_passwd = hashlib.sha512(passwd + salt).hexdigest()

            NewsDatabase.execute("""UPDATE usersTable SET password=%s WHERE
                    email=%s""", hashed_passwd, email)
            NewsDatabase.execute("""UPDATE saltTable SET salt=%s WHERE
                    email=%s""", salt, email)
            return True
        else:
            return False

    @classmethod
    def change_name(self, name, new_name):
        print 'name: ', name
        print 'new_name: ', new_name
        if new_name and not myTools.is_name_exist(new_name):
            print 'hehe'
            NewsDatabase.execute("""UPDATE usersTable SET name=%s WHERE
                name=%s""", new_name, name)
            return True
        return False
            
