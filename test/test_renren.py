#!/usr/bin/env python
#-*- coding: utf-8 -*-

from renren import RenRen

renren = RenRen()
renren.login("pedestal_peter@163.com", "pedestaldlut")

s = "ceshi"
print renren.postStatus(s)['msg']
