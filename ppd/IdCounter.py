#coding=utf8

__author__ = 'luocheng'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from mongoengine import *
class WebPage(Document):
    docid = IntField()
    valid=BooleanField()
    time  = StringField()
    content = StringField()

connect('ppdcrawler', host='127.0.0.1', port=27017)

ids = set()
for w in WebPage.objects:
    
    ids.add(w.docid) 
print len(ids)