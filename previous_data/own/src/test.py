__author__ = 'luocheng'


import urllib2

fout = open('../data/test.html','w')
fout.write(urllib2.urlopen('http://invest.ppdai.com/loan/info?id=460001').read())
fout.close()