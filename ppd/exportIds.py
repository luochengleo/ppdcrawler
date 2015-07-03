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

connect('ppdcrawler', host='172.29.33.103', port=27017)

fout = open('id.html','w')
for w in WebPage.objects:
    
    fout.write(str(w.docid)+'\n')
fout.close()