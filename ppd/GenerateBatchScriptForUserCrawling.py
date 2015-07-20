from mongoengine import *

alltasks = set()
finished = set()

class User(Document):
    userid = StringField()
    valid=BooleanField()
    time  = StringField()
    content = StringField()

connect('ppduser', host='127.0.0.1', port=27017)
count = 0
qset =  User.objects()
while True:
	try:
		count +=1
		if count %1000==0:
			print count
		w = qset.next()
		if w==None:
			break
		else:
			finished.add(w.userid)
	except:
		break
for i in range(0,32,1):
	for l in open('../config/user'+str(i)+'.task').readlines():
		alltasks.add(l.strip())

count = 0
for item in alltasks:
	if item not in finished:
		count +=1
		if count %100 ==0:
			print 'writing...',count
		open('../config/new/user'+str(count % 32)+'.task','a').write(str(item)+'\n')