# coding:utf-8
import sys
import requests
import time  
from datetime import datetime  

url = "http://www.firefoxchina.cn/"
RequestMax = 100
RequestTime = 0

if(len(sys.argv) == 3):
    url=sys.argv[1]
    RequestMax=int(sys.argv[2])
    

print len(sys.argv)

for i in range(0,RequestMax):
    start_ = datetime.utcnow()
    #try:
    r = requests.get(url)
    #except requests.exceptions.ConnectTimeout:
        #break
    end_ = datetime.utcnow() 
    c = (end_ - start_)
    RequestTime = RequestTime + c.microseconds
    print i
    print "request time: " + str(c.microseconds)
    print "request stat: " + str(r.status_code)
print "Avarage http request(%s) time=%d" % (url,RequestTime/RequestMax)
