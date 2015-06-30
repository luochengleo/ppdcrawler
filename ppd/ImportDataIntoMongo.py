#coding=utf8
__author__ = 'luocheng'

import sys

from mongoengine import *

class WebPage(Document):
    docid = IntField()
    valid=BooleanField()
    time  = StringField()
    content = StringField()

connect('ppdcrawler', host='127.0.0.1', port=27017)

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
fout = open('mv_files.bat','w')
count = 0
for f in os.listdir('datas/pages'):
    count +=1

    if '.html' in f:
        print count,f
        _,id,time = f.replace('.html','').split('_')
        wp = WebPage(docid = int(id),valid=True,time=time,content=open('datas/pages/'+f).read())
        fout.write('mv ./datas/pages/'+f+' '+'./datas/archieve\n')
        wp.save()
fout.close()

