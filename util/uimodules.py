#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado
import util.myTools as myTools

class Pagination(tornado.web.UIModule):
    def render(self, total_pages, current_page, visible_pages):
        return self.render_string("pagination.html", total_pages=total_pages,
                current_page=current_page, visible_pages=visible_pages)

    def javascript_files(self):
        return ["/static/script/jquery.twbsPagination.js",
                "/static/script/pagination-init.js"]

class Banner(tornado.web.UIModule):
    def render(self, slides):
        return self.render_string("banner.html", slides=slides)

class Navbar(tornado.web.UIModule):
    def render(self, brand, navs, user, login_state):
        return self.render_string("navbar.html", brand=brand, navs=navs,
                user=user, login_state=login_state)

class NavbarPedestal(Navbar):
    def render(self, user, url, login_state):
        brand = {}
        brand['href'] = '/'
        brand['name'] = 'Pedestal'

        navs = [{}, {}, {}]
        navs[0]['name'] = '项目实验室'
        navs[0]['href'] = '/project'
        navs[1]['name'] = '周知新闻'
        navs[1]['href'] = '/index'
        navs[2]['name'] = '关于我们'
        navs[2]['href'] = '/about'
        if url == '/':
            brand['active'] = True
        elif url == '/index':
            navs[1]['active'] = True
        elif url == '/about':
            navs[2]['active'] = True

        name = {}
        if user.has_key('vip'):
            name['name'] = user['vip']['name']
            name['id'] = myTools.get_id_by_name(name['name'])
        elif user.has_key('guest'):
            name['name'] = 'Guest:' + user['guest']['name']
            name['id'] = myTools.get_id_by_name(name['name']) 

        return Navbar.render(self, brand, navs, name, login_state) 

class List(tornado.web.UIModule):
    def render(self, lid, lclass, elements):
        return self.render_string("list.html", lid=lid, lclass=lclass, elements=elements)
