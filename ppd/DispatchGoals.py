#coding=utf8
import sys 
begin,end,targets = sys.argv[1:]
if targets=='nus' or targets == 'nas':
	style = 'win'
if targets == 'thuir':
	style = 'linux'

filename = '.'.join(['run',begin,end, targets])
if style == 'win':
	filename = filename+'.bat'
else:
	filename = filename +'.sh'

fout = open(filename,'w')
for i in range(0,4,1):
	if style =='win':
		fout.write('start python AutoCrawler.py '+begin+' '+end+' '+str(i)+'\n' )
	if style =='linux':
		fout.write('nohup python AutoCrawler.py '+begin+' '+end+' '+str(i)+' > '+str(i)+'.log &'+'\n' )

fout.close()