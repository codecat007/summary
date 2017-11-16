#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

url_pre = "http://sec.huawei.com/sec/web/viewIps.do?id="
url_id = 1

for i in range(1,10000):
    url = url_pre + str(url_id)
    html = "ips" + str(url_id) + ".html"
    #print "wget: " + url
    cmd = "wget --header='Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3' " + url + " -O " + html
    print cmd
    os.system(cmd); 
    url_id =  url_id + 1
