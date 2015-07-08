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
count = 0
qset =  WebPage.objects(docid__gt=2950000)
while True:
    w = qset.next()
    print w.docid

    fout = open('datas/pages3/'+str(w.docid)+'.html','w')
    fout.write(w.content)
    print w.docid
    fout.close()