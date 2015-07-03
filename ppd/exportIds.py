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

fout = open('id.txt','w')
wset = WebPage.objects
while True:
    w = wset.next()
    if w!=None:
        fout.write(str(w.docid)+'\n')
    else:
        break

fout.close()