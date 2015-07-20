#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

attr = open('attribute.csv','w')
attr.write('"债务id","属性","属性内容"\n')
for i in range(0,8,1):
	for l in open('attr_info'+str(i)+'.csv').readlines():
		segs = l.strip().split(',')
		attr.write(','.join([segs[0],segs[1],'"'+''.join(segs[2:])])+'\n')

attr.close()

bid = open('bid.csv','w')
bid.write('"债务id", "投标人","当年利率","有效金额","投标时间"\n')
for i in range(0,8,1):
	for l in open('bid_info'+str(i)+'.csv').readlines():
		bid.write(l)
bid.close()

user = open('user.csv','w')
user.write('"债务id","借款目的","性别","年龄","婚姻情况","文化程度","住宅状况","是否购车"\n')

for i in range(0,8,1):
	for l in open('user_info'+str(i)+'.csv').readlines():
		user.write(l)
user.close()

general = open('general.csv','w')
general.write('"抓取时间","债务id","安","非","赔","保","农","订单标题","发布者id","信用评级","发布者历史","金额","收益率","还款方式","还款细节","进度条","投标情况","结束时间","投标状态"\n')

for i in range(0,8,1):
	for l in open('general_info'+str(i)+'.csv').readlines():
		general.write(l)
general.close()
