# coding:utf-8
import requests
import time  
from datetime import datetime  

url = "https://www.baidu.com/"
RequestMax = 100
RequestTime = 0


for i in range(0,RequestMax):
	start_ = datetime.utcnow()
	r = requests.get(url)
	end_ = datetime.utcnow() 
	c = (end_ - start_)
	RequestTime = RequestTime + c.microseconds
	print i
	print "request time: " + str(c.microseconds)
	print "request stat: " + str(r.status_code)
print "Avarage http request time: " + str(RequestTime/RequestMax)
