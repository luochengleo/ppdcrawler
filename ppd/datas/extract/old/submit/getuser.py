fin = open('general.csv')

fout = open('alluserid.dat','w')

users = set()
count = 0
for l in fin.readlines()[1:]:
	segs = l.strip().split('","')
	if len(segs)>=9:
		user = segs[8].replace('"','')
		users.add(user)
count = 0
for u in users:
	count +=1
	open('user'+str(count%16)+'.task','a').write(u+'\n')

