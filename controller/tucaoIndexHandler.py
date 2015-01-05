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

class TucaoIndexHandler(myTools.BaseHandler):
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

