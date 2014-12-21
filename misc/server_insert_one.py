#!/usrebin/env python
#-*- coding: utf-8 -*-

from db import *
from config import *
from myTools import *

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    nid = raw_input('Input nid:')
    myTools.add_news(nid)
