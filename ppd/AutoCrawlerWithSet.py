# -*- coding: utf-8 -*-

import urllib, urllib2, cookielib
import sys, string, time, os, re
import csv
from bs4 import BeautifulSoup
import socket, errno

import random
from tools_ppdai import *
from mongoengine import *


headers={'Referer':'http://www.ppdai.com/default.htm','User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)', 'Host':'www.ppdai.com'}

#全局变量

class WebPage(Document):
    docid = IntField()
    valid=BooleanField()
    time  = StringField()
    content = StringField()

def getData_ppdai(url, filedirectory,mod):
    global rows_sheet
    global writers

    starttime = time.clock()
    lostPageCount = int(0) #记录连续404的页面个数，若该数值大于LOST_PAGE_LIMIT，则认为已录完数据
    fileCount = 0

    '''创建log文件'''
    strtime = str(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
    
    files = []
    
    tasks = list()
    finished = set()
    exception = set()
    for l in open('../config/'+str(mod)+'.task','r'):
        if l.strip().isdigit():
            tasks.append(int(l.strip()))
    random.shuffle(tasks)
    for l in open('../config/'+str(mod)+'.finished','r'):
        if l.strip().isdigit():
            finished.add(int(l.strip()))
    for l in open('../config/'+str(mod)+'.exception','r'):
        if l.strip().isdigit():
            exception.add(int(l.strip()))
    lastpage = tasks[0] - 1 #记录抓取的最后一个有效页面




    _count = 0
    for i in tasks:
        _count +=1
        if _count %10== 0:
            _fout = open('../config/'+str(mod)+'.finished','w')
            for _f in finished:
                _fout.write(str(_f)+'\n')
            _fout.close()
            print len(finished), ' of ', len(tasks),' tasks done.'

        if i not in finished and i not in exception:
            req = urllib2.Request(url+str(i), None, getRandomHeaders())
            try:
                response = urllib2.urlopen(req)
                r = re.search(str(i), response.geturl())
                if not r:
                    open('../config/'+str(mod)+'.exception','a').write(str(i)+'\n')
                    exception.add(i)
                    print(str(i)+': Page Redirected!')
                    continue

                m = response.read()
                lastpage = i
            except (urllib2.URLError) as e:
                if hasattr(e, 'code'):
                    print 'ERROR CODE',e.code
                if hasattr(e, 'code') and e.code == 404:
                    open('../config/'+str(mod)+'.exception','a').write(str(i)+'\n')
                    exception.add(i)
                    lostPageCount = lostPageCount + 1
                    if(lostPageCount > LOST_PAGE_LIMIT):
                        print('YOU HAVE GOT THE LASTEST PAGE!')
                        break
                    else:
                        continue #only a few pages are lost
                elif hasattr(e, 'code') and e.code == 403:
                    login()
                    open('../config/'+str(mod)+'.exception','a').write(str(i)+'\n')
                    i = lastpage
                    continue
                else:
                    if hasattr(e, 'code'):
                        print(str(e.code)+': '+str(e.reason))
                    else:
                        print(str(e.reason))
                    i = lastpage
                    continue
            except socket.error as e:
                print('[ERROR] Socket error: '+str(e.errno))
                if e.errno == 10054: #被服务器端强行关闭
                    print('[ERROR] Socket was closed by the server.\n Trying to reconnect...')
                #将最新页面写入log文件中

                time.sleep(CLOSE_WAIT_TIME)
                login()
                i = lastpage #重新获取最新页面
                continue

            #end try&except
            response.close()
            lostPageCount = 0

            '''writing files'''
            strtime = str(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
            sName = filedirectory + dataFolder + 'order_'  + str(i).zfill(LIST_LENGTH) +'_'+strtime+ '.html'
            print('Downloading ' + str(i) + ' web page...')

            #保存网页文件
            wp = WebPage(docid = int(i),valid=True,time=strtime,content=str(m))
            wp.save()
            finished.add(i)
            print 'Insert ',i,' into MongoDB'
            
    endtime = time.clock()
    print(u"[file number]:"+str(fileCount))
    print(u'[execute time]:'+str(endtime - starttime))
    _fout = open('../config/'+str(mod)+'.finished','w')
    for _f in finished:
        _fout.write(str(_f)+'\n')
    _fout.close()
    print len(finished), ' of ', len(tasks),' tasks done.'
    return


reload(sys)
sys.setdefaultencoding('utf-8') #系统输出编码置为utf8，解决输出时的乱码问题

filedirectory = getConfig()

print '************************************'
print '* Paipaidai Auto Loan Spider v0825 *'
print '************************************'

createFolder(filedirectory)
createFolder(filedirectory+dataFolder)
createFolder(filedirectory+userFolder)
getProxyList()
connect('ppdcrawler', host='172.29.33.103', port=27017)


import sys

mod = int(sys.argv[1])

print('Data Path: '+filedirectory)
if login():
    #setProxy()
    tempCount = 0
    while True:
        print 'Current Url:',ppdaiurl
        try:
            getData_ppdai(ppdaiurl, filedirectory, mod)
        except:
            pass
