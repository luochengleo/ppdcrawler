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

for w in WebPage.objects:
    fout = open('datas/pages2/'+str(w.docid)+'.html','w')
    fout.write(w.content)
    print w.docid
    fout.close()