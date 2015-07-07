__author__ = 'luocheng'
import time
from bs4 import BeautifulSoup
from bs4 import *



def analyzeData_ppdai(orderID, webcontent, writers):
    soup = BeautifulSoup(webcontent)
    #print soup.__class__
    #print(soup.original_encoding)
    #soup.prettify()
    #print(soup)

    ##————————————sheet1 begin————————————————————
    buffer1 = []
    ##抓取时间（0）
    nowtime = time.localtime(time.time())
    getdate = str(time.strftime('%Y/%m/%d', nowtime))
    buffer1.append(getdate)
    gettime = str(time.strftime('%H:%M:%S', nowtime))
    buffer1.append(gettime)

    ##订单号（1）
    buffer1.append(orderID)


    ##订单类型（2）:安（应收款安全标）/非（非体现标）/赔（审错就赔付标）/保（个人担保标）/农（助农计划）
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

    buffer1.append(an)
    buffer1.append(fei)
    buffer1.append(pei)
    buffer1.append(bao)
    buffer1.append(nong)

    #标题(3)
    tag_title = soup.find('td', {'class':'list_tit'})
    title = tag_title.find('h1').string
    #print(title)
    #logfile.write(title.encode('gbk')+',')
    buffer1.append(title)

    ##金额（4）
    tag_amount = soup.find('span', {'id':'TotalAmount'})
    amount = re.search(r'\d+(,\d+)?', tag_amount.string)
    if amount:
        amount = amount.group().replace(',', '') #删除数字中的逗号
        #logfile.write(amount+',')
        buffer1.append(amount)
    else:
        #logfile.write('NA,')
        buffer1.append('')

    ##年利率（5）
    tag_interestRate = soup.find('label', text=re.compile(u'年利率：'))
    #print(tag_interestRate)
    interestRate = tag_interestRate.find_next_sibling('span').string
    interestRate = re.search(r'\d+', interestRate).group()
    #print(interestRate)
    buffer1.append(interestRate)

    ##期限（6）
    #tag_timeLimit = soup.find(text=re.compile(u'\w*限：'))
    #ATTENTION!!!!!
    tag_timeLimit = soup.find('label', text=re.compile(u'期(\u00A0)*限：'))
    #print(tag_timeLimit.string.encode('utf-8'))
    timeLimit = tag_timeLimit.find_next_sibling('span').string
    timeLimit_months = re.search(r'\d+', timeLimit)
    if timeLimit_months:
        #logfile.write(timeLimit_months.group()+',')
        buffer1.append(timeLimit_months.group())
    else:
        #logfile.write('NA,')
        buffer1.append('')

    #print(buffer1)

    ##还款方式（7）
    p = re.compile(u'.*(，每月还款|月还息|一次还本付息).*')
    tag_refund = soup.find(text = p)
    tag_refund = tag_refund.strip()
    #print(tag_refund)
    p = re.compile(u'：')
    m = p.split(tag_refund)
    buffer1.append(m[0])


    ##每月还款金额（8）
    if len(m) > 1:
        temp = m[1].replace(',', '')
        refund = re.search(r'\d+', temp)
        if(refund):
            refund = refund.group()
        else:
            refund = ''
    else:
        refund = ''
    buffer1.append(refund)

    ##进度(9)
    tag_progress = soup.find('div', {'id':'progress'})
    progress = re.search(r'\d+(\.\d+)?', tag_progress.string).group()
    buffer1.append(progress)

    ##借款状态（10）
    tag_state = soup.find(['a','span'], text=re.compile(u'\s*(借款成功|借款审批中|正在预审|投标已结束)\s*'))
    if tag_state:
        state = tag_state.string.strip()
    else:
        state = ''
    buffer1.append(state)

    #print(tag_success)
    ##剩余时间、结束时间（11）
    tag_leftTime = soup.find('span', {'id':'leftTime'})
    leftTime = tag_leftTime.string.strip()
    matchFinishTime =re.search(u'结束时间：(\d+/\d+/\d+)', leftTime)
    if matchFinishTime:
        finishTime = matchFinishTime.group(1)
        #print finishTime
        leftTime = ''
    else:
        finishTime = ''
    buffer1.append(leftTime)
    buffer1.append(finishTime)

    ##总投标数、浏览量（12）
    tag_investNumber = soup.find(text=re.compile(u'总投标数：(\d+)(\s|\n)*\| 浏览量：(\d+)'))
    m = re.search(u'总投标数：(\d+)(\s|\n)*\| 浏览量：(\d+)', tag_investNumber)
    investNumber = m.group(1)
    viewNumber = m.group(3)
    buffer1.append(investNumber)
    buffer1.append(viewNumber)

    #借款id(13)
    tag_UserName = soup.find('div', {'class':'user_face_name'})
    userName = tag_UserName.a.string
    #logfile.write(userName+',')
    buffer1.append(userName)
    #print(str(userName.string)+'\n')

    #借入信用等级（14）
    tag_borrowRank = soup.find('i', {'title':'信用等级'})
    if tag_borrowRank:
        borrowRank = tag_borrowRank['class']
        buffer1.append(borrowRank[0])
    else:
        buffer1.append("")

    #借入信用分数（15）
    tag_borrowScore = soup.find('label', text=re.compile(u'(\s|\n)*借入信用：'))
    #tag_borrowScore = tag_borrowRank.next_sibling #'   （28）分   '
    #print(tag_borrowScore)
    borrowScore = re.search(u'\d+', tag_borrowScore.parent.get_text())
    if borrowScore:
        borrowScore = borrowScore.group()
        #print borrowScore
    else:
        borrowScore = 0
    buffer1.append(borrowScore)

    #借出信用分数（16）
    tag_lendScore = soup.find('p', text=re.compile(u'(\s|\n)*借出信用：\.*'))
    lendScore = re.search(r'\d+', tag_lendScore.string).group()
    buffer1.append(lendScore)

    #成功次数（17）
    tag_timesOfSuccessAndFail = soup.find('h3', text=re.compile(u'\.*次成功，\d+ 次流标\.*'))
    #print(tag_timesOfSuccessAndFail)
    m = re.findall(r'\d+', tag_timesOfSuccessAndFail.string.strip())
    timesOfSuccess = m[0]
    buffer1.append(timesOfSuccess)

    #流标次数（18）
    timesOfFail = m[1]
    buffer1.append(timesOfFail)

    #身份认证（19）
    tag_hukou = soup.find('i', {'class':'hukou'})
    if tag_hukou:
        hukouIdentify = 1
    else:
        hukouIdentify = 0
    buffer1.append(hukouIdentify)
    #视频认证（20）
    tag_video = soup.find('i', {'class':'video'})
    if tag_video:
        videoIdentify = 1
    else:
        videoIdentify = 0
    buffer1.append(videoIdentify)
    #学历认证（21）
    tag_record = soup.find('i', {'class':'record'})
    if tag_record:
        recordIdentify = 1
    else:
        recordIdentify = 0
    buffer1.append(recordIdentify)

    #手机认证（22）
    tag_phone = soup.find('i', {'class':'phone'})
    if tag_phone:
        phoneIdentify = 1
    else:
        phoneIdentify = 0
    buffer1.append(phoneIdentify)

    ##借款目的（23）
    ##性别（24）
    ##年龄（25）
    ##婚姻状况（26）
    ##文化程度（27）
    ##住宅状况（28）
    ##是否购车（29）
    tag_table = soup.find('th', text=re.compile(u'(\s|\n)*借款目的(\s|\n)*'))
    if tag_table:
        tag_table = tag_table.parent.find_next_sibling('tr').find_all('td')
        #print(len(tag_table))
        purpose = tag_table[0].string.strip()
        sex = tag_table[1].string.strip()
        age = tag_table[2].string.strip()
        marriage = tag_table[3].string.strip()
        degree = tag_table[4].string.strip()
        house = tag_table[5].string.strip()
        car = tag_table[6].string.strip()
    else:
        purpose = sex = age = marriage = degree = house = car = ''
    buffer1.append(purpose)
    buffer1.append(sex)
    buffer1.append(age)
    buffer1.append(marriage)
    buffer1.append(degree)
    buffer1.append(house)
    buffer1.append(car)

    #户口认证、学历认证、网站认证
    hukouPlace = schoolName = eduBgd = eduType = ''
    tag_hukouPlace = soup.find('span', {'class':'hukou'})
    if tag_hukouPlace:
        hukouPlace = re.search(u'户口所在地：(.*)', tag_hukouPlace.string).group(1)

    tag_school = soup.find('span', {'class':'record'})
    if tag_school:
        eduRecord = re.search(u'毕业学校：(.*)，学历：(.*)，学习形式：(.*)）', tag_school.string)
        if eduRecord:
            schoolName = eduRecord.group(1)
            eduBgd = eduRecord.group(2)
            eduType = eduRecord.group(3)

    buffer1.append(hukouPlace)
    buffer1.append(schoolName)
    buffer1.append(eduBgd)
    buffer1.append(eduType)

    tag_siteAuth = soup.find('h4', text=u'网站认证：')
    rank_taobao = taobao = ''
    if tag_siteAuth:
        siteAuth = 1
        list_taobao = tag_siteAuth.find_next_siblings('span', {'class':'taobao'})#可能有多条
        if len(list_taobao) > 0:
            taobao = 1
            guanCount = zuanCount = 0
            for item_taobao in list_taobao:
                guanCount += len(item_taobao.find_all('img', {'src':'http://static.ppdai.com/skin/images/sell_guan.gif'}))
                zuanCount += len(item_taobao.find_all('img', {'src':'http://static.ppdai.com/skin/images/sell_zhuan.gif'})) #写网站的人z/zh不分
            rank_taobao = guanCount*10+zuanCount
            m_tmall = re.search(u'天猫商城', unicode(list_taobao))
            if m_tmall:
                rank_taobao = u'天猫商城'
        else:
            taobao = 0
    else:
        siteAuth = 0
    buffer1.append(siteAuth)
    buffer1.append(taobao)
    buffer1.append(str(rank_taobao))
    #print(tag_table)
    #tag_basicInfo = tag_table.find_next_sibling('tr')
    #print(tag_basicInfo)

    ##关于我（30）
    tag_aboutme = soup.find('h3', text=re.compile(u'(\s|\n)*关于我(\s|\n)*'))
    #print(tag_aboutme.next_sibling.next_sibling)
    if tag_aboutme:
        aboutme = tag_aboutme.find_next_sibling('p').string
        if aboutme:
            aboutme = aboutme.strip()
            aboutme = aboutme.replace(u'\u000D\u000A', '') #删除换行
    else:
        aboutme = ''
    ##我想要使用这笔款项做什么（31）
    tag_wanttodo = soup.find('h3', text=re.compile(u'(\s|\n)*我想要使用这笔款项做什么(\s|\n)*'))
    if tag_wanttodo:
        wanttodo = tag_wanttodo.find_next_sibling('p').string
        if wanttodo:
            wanttodo = wanttodo.strip()
            wanttodo = wanttodo.replace(u'\u000D\u000A', '') #删除换行
    else:
        wanttodo = ''
    ##我的还款能力说明（32）
    tag_refundAbility = soup.find('h3', text=re.compile(u'(\s|\n)*我的还款能力说明(\s|\n)*'))
    if tag_refundAbility:
        refundAbility = tag_refundAbility.find_next_sibling('p').string
        if refundAbility:
            refundAbility = refundAbility.strip()
            refundAbility = refundAbility.replace(u'\u000D\u000A', '') #删除换行
    else:
        refundAbility = ''

    buffer1.append(aboutme)
    buffer1.append(wanttodo)
    buffer1.append(refundAbility)

    #将数据写入表1中
    writers[0].writerow(buffer1)
    '''
    sheet1 = excelbook.get_sheet(0)
    col = 0
    #row = excelbook.sheet_by_index(0).nrows
    buffer11 = []
    for item in buffer1:
        sheet1.write(rows_sheet[0], col, item)
        col += 1
        #buffer11.append(item.decode('gbk'))
    rows_sheet[0] += 1 #行数加1
    '''
    ##————————————sheet1 finish————————————————————

    ##————————————sheet2  begin————————————————————
    #sheet2 = excelbook.get_sheet(1)
    tag_investList = soup.find('th', text=re.compile(u'(\s|\n)*投标人(\s|\n)*'))
    if tag_investList:
        '''
        lastItem = tag_investList.parent
        count = 0;
        while True:
            count += 1
            investItem = lastItem.find_next_sibling('tr')
            lastItem = investItem
            #print(count)
        '''
        investList = tag_investList.parent.find_next_siblings('tr')
        #print("length: "+str(len(investList)));
        #print investList
        for investItem in investList:
            investInfo = investItem.find_all('td')

            if(len(investInfo)<4):
                break;
            #投标ID
            invest_id = investInfo[0].find('a').string.strip()
            #当前利率
            invest_rate = investInfo[1].string.strip()
            invest_rate = re.search(u'\d+', invest_rate).group()
            #投标金额
            invest_amount = investInfo[2].string.strip()
            invest_amount = re.search(r'\d+(,\d+)?', invest_amount)
            invest_amount = invest_amount.group().replace(',', '') #删除数字中的逗号
            #投标时间
            invest_time = investInfo[3].string.strip()
            m = re.search(u'(\d+/\d+/\d+) (\d+:\d+:\d+)', invest_time)
            invest_day = m.group(1)
            invest_second = m.group(2)

            buffer2 = []
            ##抓取时间（0）
            nowtime = time.localtime(time.time())
            getdate = str(time.strftime('%Y/%m/%d', nowtime))
            buffer2.append(getdate)
            gettime = str(time.strftime('%H:%M:%S', nowtime))
            buffer2.append(gettime)
            buffer2.append(orderID) #订单号
            buffer2.append(invest_id)
            buffer2.append(invest_rate)
            buffer2.append(invest_amount)
            buffer2.append(invest_day)
            buffer2.append(invest_second)

            writers[1].writerow(buffer2)
