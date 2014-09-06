#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.httpclient
import json

data = {}
data['access_token'] = "265124|6.50b9b1a3fc3e3268dbfb82d1e56d52ae.2592000.1396522800-584618426"
data['status'] = "ceshi"
data['format'] = "json"
data['method'] = "status.set"
data['page_id'] = "601037056"
data['v'] = "1.0"

json = json.dumps(data)
print json

url = "https://api.renren.com/v2/status/put"
url = "https://api.renren.com/restserver.do"
request = tornado.httpclient.HTTPRequest(url=url, method="POST", body=json)
client = tornado.httpclient.HTTPClient()
response = client.fetch(request)
print response.body
