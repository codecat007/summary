import urllib2  
import re  
import requests  
import sys  
  
import urllib  
reload(sys)  
sys.setdefaultencoding('utf-8')  
type = sys.getfilesystemencoding()  
r = urllib.urlopen("http://sec.huawei.com/sec/web/viewIps.do?id=9214")  
a = r.read().decode('utf-8').encode(type)  
print a 
