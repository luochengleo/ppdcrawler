for i in range(0,32,1):
	open('user'+str(i)+'.finished','w').close()
	open('user'+str(i)+'.exception','w').close()
	open('../ppd/run.bat','a').write('start python AutoUserCrawlerWithSet.py '+str(i)+'\n')
