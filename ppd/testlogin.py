from tools_ppdai import *

filedirectory = getConfig()
getProxyList()


if login():
	print 'success'
else:
	print 'fail'