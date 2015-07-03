__author__ = 'luocheng'

finish = set()
for l in open('id.txt').readlines():
    finish.add(int(l.strip()))

_count = 0
for i in range(460000,3000000,1):
    if i not in finish:
        _count +=1
        fout = open('../config/'+str(_count % 16)+'.task','a')
        fout.write(str(i)+'\n')
        fout.close()
for i in range(0,16,1):
    fout = open('../config/'+str(i)+'.finished','w')
    fout.write('\n')
    fout.close()
    open('run'+str(i%4)+'.bat','a').write('start python AutoCrawlerWithSet.py '+str(i)+'\n')

