# -*- coding: utf-8 -*-
import os,sys
from random import randint
import re
import time
import urllib2
import socket, errno


URL_PREFIX= u'http://invest.ppdai.com/loan/info?id='
ipAddress = ['166.5.31.177', '191.234.5.2', '178.98.246.45, 231.67.9.23']
host = 'www.ppdai.com'
userAgent = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36']

headers={'Referer':'http://www.ppdai.com/default.htm','User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)', 'Host':'www.ppdai.com'}
pageDir =u'../data/pages'
LAST_CRAWLED_PAGE = 1
MAX_PAGE=3000000
LOST_PAGE_LIMIT = 10
CLOSE_WAIT_TIME = int(100) #爬虫被服务器强行关闭后的等待时间
LIST_LENGTH = int(6)

def login():
    cj = cookielib.CookieJar()
    print("Current proxy: "+proxyList[0])
    proxy_handler = urllib2.ProxyHandler({"http": proxyList[0]})
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy_handler)
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #opener.addheaders = headers
    urllib2.install_opener(opener)

    data = {'UserName':username, 'Password':password, 'Continue':'/default'}
    postdata = urllib.urlencode(data)

    try:
        req = urllib2.Request(urlAuth, postdata, headers = getRandomHeaders())
        #req.set_proxy('111.206.81.248:80', 'http')
        result = urllib2.urlopen(req)
        result.close()
        #for index, cookie in enumerate(cj):
        #    print '[',index,']',cookie

        req2 = urllib2.Request(urlAccount, headers = getRandomHeaders())
        #req2.set_proxy('111.206.81.248:80', 'http')
        result2 = opener.open(req2)
        result2.close()
        return True
    except (urllib2.URLError) as e:
        print("Login Failed!")
        if hasattr(e, 'code'):
            print('ERROR:'+str(e.code)+' '+str(e.reason))
        else:
            print(str(e.reason))
    except socket.error as e:
        print('[ERROR] Socket error: '+str(e.errno))
    except:
        print(u'[FAIL]Login failed. Please try again!')
        return False

def init_dirs():
    if 'pages' in os.listdir('../data'):
        pass
    else:
        os.mkdir('../data/pages')

    if 'users' in os.listdir('../data'):
        pass
    else:
        os.mkdir('../data/users')

def init_params():
    pass


def getRandomHeaders():
    ipNumber = len(ipAddress)
    agentNumber = len(userAgent)
    headers = {'User-Agent': userAgent[randint(0, agentNumber-1)], 'Host': host, 'X-Forwarded-For': ipAddress[randint(0, ipNumber-1)]}
    return headers


def getData_ppdai(url, begin_page, end_page=MAX_PAGE):
    global rows_sheet
    global writers

    print(u'\nSTART to get webpages from: '+str(begin_page))
    starttime = time.clock()
    lostPageCount = int(0) #记录连续404的页面个数，若该数值大于LOST_PAGE_LIMIT，则认为已录完数据
    fileCount = 0

    strtime = str(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))

    files = []
    writers = [] #清空原有csv writers


    lastpage = begin_page - 1 #记录抓取的最后一个有效页面


    for i in range(begin_page, end_page+1):
        lastlastpage = lastpage #用于判断lastpage是否更新
        req = urllib2.Request(url+str(i), None, getRandomHeaders())
        try:
            print 'CRAWLING',url+str(i)
            #response = responseFromUrl(url+str(i))
            #req.set_proxy(proxyList[0], 'http')
            response = urllib2.urlopen(req)
            #部分页面会重定向到/default.html，（如400001），以此来判定
            r = re.search(str(i), response.geturl())
            if not r:
                print(str(i)+': Page Redirected!')
                continue

            m = response.read()
            lastpage = i
        except (urllib2.URLError) as e:
            print 'URLERROR'
            if hasattr(e, 'code'):
                print e.code
            if hasattr(e, 'code') and e.code == 404:
                lostPageCount = lostPageCount + 1
                if(lostPageCount > LOST_PAGE_LIMIT):
                    print('YOU HAVE GOT THE LASTEST PAGE!')
                    break
                else:
                    continue #only a few pages are lost
            elif hasattr(e, 'code') and e.code == 403:
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

            #等待一定时间后重新连接
            time.sleep(CLOSE_WAIT_TIME)
            i = lastpage #重新获取最新页面
            continue

        #end try&except
        response.close()
        lostPageCount = 0

        '''writing files'''
        strtime = str(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
        sName = pageDir + '/order_'  + str(i).zfill(LIST_LENGTH) +'_'+strtime+ '.html'
        print('Downloading ' + str(i) + ' web page...')

        #保存网页文件
        f = open(sName, 'wb')
        f.write(m)
        f.close()



    endtime = time.clock()
    print(u"[file number]:"+str(fileCount))
    print(u'[execute time]:'+str(endtime - starttime))
    return

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8') #系统输出编码置为utf8，解决输出时的乱码问题
    init_dirs()
    getData_ppdai(URL_PREFIX,460001)
