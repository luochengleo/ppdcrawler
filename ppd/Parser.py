#coding=utf8


__author__ = 'luocheng'
from bs4 import BeautifulSoup
import time
import re

def analysisTab(tab):
    rtr =dict()
    attrname = ''
    content = ''

    for c in tab.children:
        if c.name =='h3':
            if attrname.strip() != '':
                rtr[attrname]= ' '.join([line.strip() for line in  content.split('\n')])
                attrname = c.get_text()
                content = ''
            else:
                attrname = c.get_text()
        if c.name == 'p':
            content += c.get_text()

    return [ '"'+str(k)+'",'+str(rtr[k])+'"' for k in rtr.keys()]

def analysisUserProfileData(table):
    if table !=None:

        alllines = list()
        for t  in table.find_all('tr')+table.find_all('th'):
            _content = ','.join([ '"'+item.get_text().strip()+'"' for item in t.find_all('td')])
            if _content.strip() !='':
                alllines.append(_content)
        return alllines
    else:
        return []
def analysisUserLoanList( table ):
    if table ==None:
        return []
    else:
        alllines = list()
        for ol in table.find_all('ol'):
            _tag = ''
            if 'fastbid' in ol.prettify():
                _tag += 'FAST'
            if 'autobid' in ol.prettify():
                _tag+='AUTO'
            if _tag == '':
                _tag = 'NONE'
            alllines.append(','.join(['"'+item.get_text().strip()+'"' for item in ol.find_all('li')])+',"'+_tag+'"')
        return alllines


def analyzeData_ppdai(docid,time, webcontent):
    # headers of table
    #抓取时间 	订单号	安	非	赔	保	农	订单标题	金额(元）	年利率	期限（月）	还款方式	每月还款金额	进度	借款状态	剩余时间	结束时间	总投标数	浏览量	借款id	借入信用等级	借入信用分数	借出信用分数	成功次数	流标次数	身份认证	视频认证	学历认证	手机认证	借款目的	性别	年龄	婚姻状况	文化程度	住宅状况	是否购车	关于我	我想要使用这笔款项做什么	我的还款能力说明
    data = list()
    data.append(time)#抓取时间
    data.append(docid)#订单号

    soup = BeautifulSoup(webcontent)

    ##订单类型（2）:安（应收款安全标）/非（非提现标）/赔（审错就赔付标）/保（个人担保标）/农（助农计划）
    an = fei = pei = bao = nong = 0
    tag_an = soup.find('i', {'class':'an'})
    if tag_an:  an = 1
    tag_fei = soup.find('i', {'class':'fei'})
    if tag_fei: fei = 1
    tag_pei = soup.find('i', {'class':'pei'})
    if tag_pei: pei = 1
    tag_bao = soup.find('i', {'class':'bao'})
    if tag_bao: bao = 1
    tag_nong = soup.find('i', {'class':'nong'})
    if tag_nong: nong = 1

    data.append(an)
    data.append(fei)
    data.append(pei)
    data.append(bao)
    data.append(nong)


    #标题(3)
    try:
        t = soup.find('span',{'tt':re.compile('\d.*?')})
        data.append(t.string)
    except:
        data.append('')
    #用户id
    userid = soup.find('a',{'class':'username'})
    data.append(userid.string)

    # user rating
    try:
        _p = re.compile('creditRating\s(\w+)')
        match =_p.search(webcontent)
        if match:
            data.append( match.groups()[0])
        else:
            data.append('')
    except:
        data.append('EXCEPTION')
    #bidinfo

    try:
        bidinfo = soup.find('span',{'class':'bidinfo'})
        data.append(bidinfo.string)
    except:
        data.append('EXCEPTION')

    ##金额，年利率，期限
    try:
        loan = soup.find('div',{'class':'newLendDetailMoneyLeft'})
        for d in loan.find_all('dd'):
            try:
                data.append(d.get_text())
            except:
                data.append('')
    except:
        for i in range(0,3,1):data.append('')

    #还款方式等信息
    try:
        loan = soup.find('div',{'class':'newLendDetailRefundLeft'})
        for _d in loan.find_all('div',{'class':'item'})[0:5]:
            text = _d.get_text()
            data.append(''.join([item.strip() for item in text.split('\n')]))
    except:
        for i in xrange(5):
            data.append('')
    #投标状态
    rawstatus = soup.find('div',{'class':'wrapNewLendDetailInfoRight'})
    if rawstatus == None:
        print 'WARNING'
    status = ''
    if 'newbidstatus_lb' in rawstatus.prettify():
        status = '投标已结束'
    if 'newbidstatus_pg' in rawstatus.prettify():
        status = '正在评估中'
    if 'newbidstatus_mb' in rawstatus.prettify():
        status = '已经满标'
    data.append(status)

    table = soup.find('table',{'class':'lendDetailTab_tabContent_table1'})
    usertable = analysisUserProfileData(table)

    table = soup.find('div',{'id':'bidTable_div'})
    bidtable = analysisUserLoanList(table)
    tab = soup.find('div',{'class':'lendDetailTab_tabContent'})
    attrtable =  analysisTab(tab)

    rtr_line =','.join(['"'+str(item)+'"' for item in data])

    return rtr_line,usertable,bidtable,attrtable


import sys
reload(sys)

sys.setdefaultencoding('utf8')

mod = int(sys.argv[1])
import os
from mongoengine import *
general_out = open('./datas/extract/general_info'+str(mod)+'.csv','w')
user_info = open('./datas/extract/user_info'+str(mod)+'.csv','w')
bid_info = open('./datas/extract/bid_info'+str(mod)+'.csv','w')
attr_info = open('./datas/extract/attr_info'+str(mod)+'.csv','w')



class WebPage(Document):
    docid = IntField()
    valid=BooleanField()
    time  = StringField()
    content = StringField()
'''
count  = 0
for f in os.listdir('./datas/pages5'):

    count +=1
    if count %10==0:
        print count

    loadid = '"0000"'
    rtr,ut,bt,at =  analyzeData_ppdai('0000','0000',open('./datas/pages5/'+f).read())
    general_out.write(rtr+'\n')
    if len(ut)>0:
        user_info.write('\n'.join([loadid+','+line for line in ut])+'\n')
    if len(bt) > 0:
        bid_info.write('\n'.join([loadid+','+line for line in bt])+'\n')
    if len(at) > 0:
        attr_info.write('\n'.join([loadid+','+line for line in at])+'\n')


'''
connect('ppdcrawler', host='172.29.33.103', port=27017)
count = 0
qset =  WebPage.objects()
while True:
    count +=1
    if count %1000==0:
        print count
    w = qset.next()
    if w ==None:
        break
    if count % 8 == mod:
        try:
            loadid = '"'+str(w.docid)+'"'
            rtr,ut,bt,at =  analyzeData_ppdai(str(w.docid),w.time,w.content)
            general_out.write(rtr+'\n')
            if len(ut)>0:
                user_info.write('\n'.join([loadid+','+line for line in ut])+'\n')
            if len(bt) > 0:
                bid_info.write('\n'.join([loadid+','+line for line in bt])+'\n')
            if len(at) > 0:
                attr_info.write('\n'.join([loadid+','+line for line in at])+'\n')
        except:
            print count,'exception'


